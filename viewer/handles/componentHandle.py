import sys
from pyqtgraph.opengl.GLViewWidget import GLViewWidget
from .baseHandle import BaseHandle

sys.path.append("..")
from objects.baseSection import BaseSection

class ComponentHandle(BaseHandle):
    def __init__(self, component:BaseSection, viewport:GLViewWidget = None):
        super().__init__()
        self._object = component
        
        self.setViewPort(viewport)
        self.initTreeItem()
        self.initObject()
        
    def initObject(self):
        pass