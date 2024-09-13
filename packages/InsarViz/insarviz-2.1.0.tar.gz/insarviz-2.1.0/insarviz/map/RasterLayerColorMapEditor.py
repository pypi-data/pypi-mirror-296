# -*- coding: utf-8 -*-

from typing import Optional

import logging

import ctypes

from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_TEXTURE_2D, GL_TEXTURE_1D,
    glClear,
    glBindTexture,
    glBindVertexArray, glUseProgram,
    glClearColor,
    glGenBuffers, glBindBuffer, glBufferData,
    GL_ARRAY_BUFFER, GL_ELEMENT_ARRAY_BUFFER, GL_STATIC_DRAW,
    glGenVertexArrays,
    glEnableVertexAttribArray,
    glVertexAttribPointer, GL_FLOAT,
    GL_TEXTURE0, glActiveTexture,
    glDrawElements, GL_TRIANGLES,
    GL_UNSIGNED_INT,
    glDeleteTextures,
)

from PyQt5.QtCore import Qt, QSize

from PyQt5.QtWidgets import (
    QDialog, QWidget, QDialogButtonBox, QVBoxLayout, QSplitter, QOpenGLWidget, QSizePolicy
)


from pyqtgraph import BarGraphItem

from pyqtgraph.colormap import ColorMap

import numpy as np

from insarviz.colormaps import create_colormap_texture

from insarviz.map.Shaders import DATA_UNIT, PALETTE_UNIT

from insarviz.map.Layer import Raster1BLayer

from insarviz.ColormapWidget import ColormapWidget, HistogramWidget

from insarviz.linalg import matrix

from insarviz.map.gl_utils import set_uniform

from insarviz.map.AbstractMapView import AbstractMapView

logger = logging.getLogger(__name__)


class RasterLayerColorMapEditor(QDialog):

    default_padding = ColormapWidget.default_padding
    max_padding = ColormapWidget.max_padding
    autorange_threshold = ColormapWidget.autorange_threshold

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)
        self.setModal(True)
        self.setWindowTitle("Edit colormap")
        self.setSizeGripEnabled(True)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.colormap: Optional[ColorMap] = None

        self.histogram_widget = HistogramWidget()
        # store the colormap itself because its name is not saved in gradient
        self.histogram_widget.gradient.menu.sigColorMapTriggered.connect(
            self.store_colormap)
        # new histogram curve
        self.hist_plot = BarGraphItem(x0=[], x1=[], y0=[], y1=[],
                                      pen=None, brush=(220, 20, 20, 100))
        self.hist_plot.setZValue(10)
        self.hist_plot.setRotation(90)
        self.histogram_widget.vb.addItem(self.hist_plot)

        self.layer_view = RasterLayerView()
        self.histogram_widget.sigLevelsChanged.connect(
            lambda _: self.layer_view.set_v0_v1(*self.histogram_widget.getLevels()))
        self.histogram_widget.gradient.menu.sigColorMapTriggered.connect(
            self.layer_view.set_colormap)

        self.button_box = QDialogButtonBox()
        self.autorange_button = self.button_box.addButton("Autorange", QDialogButtonBox.ResetRole)
        self.autorange_button.clicked.connect(self.autorange)
        self.cancel_button = self.button_box.addButton(QDialogButtonBox.Cancel)
        self.cancel_button.clicked.connect(self.reject)
        self.apply_button = self.button_box.addButton(QDialogButtonBox.Apply)
        self.apply_button.clicked.connect(self.accept)

        self.main_widget = QSplitter(Qt.Horizontal)
        self.main_widget.setChildrenCollapsible(False)
        self.main_widget.addWidget(self.layer_view)
        self.main_widget.addWidget(self.histogram_widget)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.main_widget)
        self.main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)

    def set_layer(self, layer: Raster1BLayer):
        assert isinstance(layer, Raster1BLayer)
        self.layer_view.set_texture(layer.textures[GL_TEXTURE0+DATA_UNIT][1], layer.model_matrix)
        self.histogram_widget.setLevels(layer.colormap_v0, layer.colormap_v1)
        self.set_colormap(layer.colormap.name)
        hist, bins = layer.histogram
        self.hist_plot.setOpts(x0=bins[:-1], x1=bins[1:], y0=np.zeros(len(hist)), y1=hist)
        ymin = float(bins[0] - (bins[-1] - bins[0]) * self.max_padding)
        ymax = float(bins[-1] + (bins[-1] - bins[0]) * self.max_padding)
        self.histogram_widget.vb.setLimits(yMin=ymin, yMax=ymax)
        self.histogram_widget.vb.setYRange(bins[1], bins[-2], padding=self.default_padding)

    def get_v0_v1(self) -> tuple[float, float]:
        return self.histogram_widget.getLevels()

    def autorange(self) -> None:
        hist = self.hist_plot.opts.get('y1')
        bins = np.empty(len(hist)+1)
        bins[:-1] = self.hist_plot.opts.get('x0')
        bins[-1] = self.hist_plot.opts.get('x1')[-1]
        v0, v1 = self.autorange_from_hist(hist, bins)
        self.histogram_widget.setLevels(v0, v1)

    autorange_from_hist = ColormapWidget.autorange_from_hist

    def set_colormap(self, name: str) -> None:
        for action in self.histogram_widget.gradient.menu.actions():
            if self.histogram_widget.gradient.menu.actionDataToColorMap(action.data()).name == name:
                action.trigger()
                return
        logger.warning(f"colormap {name} not found, switch to greyscale")
        self.set_default_colormap()

    def store_colormap(self, cmap: ColorMap) -> None:
        self.colormap = cmap

    def get_colormap(self) -> ColorMap:
        return self.colormap

    def set_default_colormap(self) -> None:
        # greyscale is the first colormap action (see colormaps.py)
        self.histogram_widget.gradient.menu.actions()[0].trigger()


class RasterLayerView(QOpenGLWidget):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setMinimumSize(QSize(640, 480))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tex_id: int = 0
        self.colormap_v0: float = 0.
        self.colormap_v1: float = 1.
        self.colormap_texid: int = 0
        self.program: int = 0
        self.vao: int = 0  # OpenGL vertex array object holding a square on which to display texture
        self.z: float = 1.0  # zoom level
        # center of the view matrix in data coordinates
        self.cx: float = 0.
        self.cy: float = 0.
        self.model_matrix: matrix.Matrix = matrix.identity()
        self.view_matrix: matrix.Matrix = matrix.identity()
        self.projection_matrix: matrix.Matrix = matrix.identity()

    def initializeGL(self) -> None:
        glClearColor(.5, .5, .5, 1.)
        # build a Vertex Array Object that is a square from (0,0) to (1,1) mapped with a texture
        # also from (0,0) to (1,1). The vertex are given in such order that:
        # glDrawArrays(GL_LINE_LOOP, 0, 4) draws the square's border
        # glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None) draws the textured square
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        data_buffer = np.ravel([
            # vertex_x, vertex_y, vertex_z, texture_x, texture_y
            [0., 0., 0., 0., 0.],
            [1., 0., 0., 1., 0.],
            [1., 1., 0., 1., 1.],
            [0., 1., 0., 0., 1.]
        ]).astype(np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ARRAY_BUFFER, data_buffer, GL_STATIC_DRAW)
        indices = np.array([0, 1, 3, 1, 2, 3], dtype='uint32')
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)
        float_size: int = ctypes.sizeof(ctypes.c_float)
        vertex_offset = ctypes.c_void_p(0 * float_size)
        tex_coord_offset = ctypes.c_void_p(3 * float_size)
        record_len: int = 5 * float_size
        glVertexAttribPointer(0, 3, GL_FLOAT, False, record_len, vertex_offset)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 2, GL_FLOAT, False, record_len, tex_coord_offset)
        glEnableVertexAttribArray(1)
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        self.program = Raster1BLayer.build_program(self)

    resizeGL = AbstractMapView.resizeGL

    def paintGL(self) -> None:
        """
        Generate and display OpenGL texture for Map.
        """
        glClear(GL_COLOR_BUFFER_BIT)
        if self.tex_id:
            glBindVertexArray(self.vao)
            # bind textures to texture units
            glActiveTexture(GL_TEXTURE0+DATA_UNIT)
            glBindTexture(GL_TEXTURE_2D, self.tex_id)
            glActiveTexture(GL_TEXTURE0+PALETTE_UNIT)
            glBindTexture(GL_TEXTURE_1D, self.colormap_texid)
            glUseProgram(self.program)
            # set view and projection matrixes
            set_uniform(self.program, 'v0', self.colormap_v0)
            set_uniform(self.program, 'v1', self.colormap_v1)
            set_uniform(self.program, 'model_matrix', self.model_matrix)
            set_uniform(self.program, 'view_matrix', self.view_matrix)
            set_uniform(self.program, 'projection_matrix', self.projection_matrix)
            # draw the two triangles of the VAO that form a square
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindTexture(GL_TEXTURE_1D, 0)
        glUseProgram(0)

    def update_view_matrix(self) -> None:
        # texture size
        tex_w, tex_h = self.model_matrix[0][0], self.model_matrix[1][1]
        self.cx, self.cy = tex_w//2, tex_h//2
        # view size
        view_w, view_h = self.width(), self.height()
        # size ratios
        view_ratio, tex_ratio = view_w / view_h, tex_w / tex_h
        if view_ratio > tex_ratio:
            # view is wider than texture
            # zoom is thus the height ratio between view and texture
            self.z = view_h / tex_h
        else:
            # view is higher than texture
            # zoom is thus the width ratio between view and texture
            self.z = view_w / tex_w
        self.view_matrix = matrix.product(
            matrix.translate(self.width()//2, self.height()//2),
            matrix.scale(self.z, self.z),
            matrix.translate(-self.cx, -self.cy)
        )

    update_projection_matrix = AbstractMapView.update_projection_matrix

    def set_texture(self, texid: int, model_matrix: matrix.Matrix) -> None:
        self.tex_id = texid
        self.model_matrix = matrix.scale(model_matrix[0][0], model_matrix[1][1])

    def set_v0_v1(self, v0: float, v1: float) -> None:
        self.colormap_v0 = v0
        self.colormap_v1 = v1
        self.repaint()

    def set_colormap(self, colormap: ColorMap) -> None:
        self.makeCurrent()
        glDeleteTextures(1, [self.colormap_texid])
        self.colormap_texid = create_colormap_texture(colormap, GL_TEXTURE0+PALETTE_UNIT)
        self.doneCurrent()
        self.repaint()
