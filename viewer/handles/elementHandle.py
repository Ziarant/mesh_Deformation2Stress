import sys
from pyqtgraph.opengl.GLViewWidget import GLViewWidget
from pyqtgraph.opengl.MeshData import MeshData
from pyqtgraph.opengl.items.GLMeshItem import GLMeshItem
from pyqtgraph.opengl.items.GLLinePlotItem import GLLinePlotItem
from .baseHandle import BaseHandle

sys.path.append("..")
from objects.baseElement import BaseElement
import numpy as np

class ElementHandle(BaseHandle):
    def __init__(self, element:BaseElement, viewport:GLViewWidget = None):
        super().__init__()
        self._object:BaseElement = element
        
        self._graphItem:GLMeshItem = GLMeshItem(drawEdges = False)
        self.graphItem.setGLOptions('opaque')
        
        color = (0.0, 0.0, 0.0, 1.0)
        self._edgeItem:GLLinePlotItem = GLLinePlotItem(color = color, antialias = True, mode = 'lines')
        self.edgeItem.setGLOptions('opaque')
        
        self.setViewPort(viewport)
        # self.initObject()
        
    def initObject(self):
        '''
        单元可视化:默认导入时不调用(占用内存较高)
        '''
        element = self.object
        vertexes, faces, edges = element.vertexes, element.faces, element.edges
        meshData = MeshData(vertexes=vertexes, faces=faces, edges=edges)
        self.graphItem.setMeshData(meshdata = meshData)
        self.viewport.addItem(self.graphItem)
        
        pos = []
        for edge in edges:
            p1, p2 = vertexes[edge[0]], vertexes[edge[1]]
            pos.append(p1)
            pos.append(p2)
        pos = np.array(pos)
        self.edgeItem.setData(pos = pos)
        self.edgeItem.setParentItem(self.graphItem)
        
    @property
    def edgeItem(self) -> GLLinePlotItem:
        return self._edgeItem