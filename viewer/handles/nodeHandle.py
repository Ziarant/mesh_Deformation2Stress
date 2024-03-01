import sys
import numpy as np
from pyqtgraph.opengl.items.GLScatterPlotItem import GLScatterPlotItem
from pyqtgraph.opengl.GLViewWidget import GLViewWidget
from .baseHandle import BaseHandle

sys.path.append("..")

class NodeHandle(BaseHandle):
    def __init__(self, node, viewport:GLViewWidget = None):
        super().__init__()
        self._object = node
        
        self._radius = 1.0
        self._graphItem = GLScatterPlotItem()
        self.graphItem.setGLOptions('opaque')
        self.graphItem.setVisible(False)
        
        self.setViewPort(viewport)
        # self.initObject()
        
    def initObject(self):
        '''
        节点可视化:默认导入时不调用(占用内存较高)
        '''
        pos = np.array([self.object.coord])
        size = np.array([self._radius])
        color = np.array([[1, 1, 1, 1]])
        self.graphItem.setData(pos=pos, size=size, color = color)
        self.viewport.addItem(self.graphItem)