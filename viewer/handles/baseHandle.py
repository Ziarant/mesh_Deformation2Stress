from PyQt5.QtWidgets import QTreeWidgetItem
from pyqtgraph.opengl.GLViewWidget import GLViewWidget
from pyqtgraph.opengl import GLGraphItem

class BaseHandle(object):
    def __init__(self):
        self._object = None
        self._treeItem = QTreeWidgetItem()
        self._viewport:GLViewWidget = None
        self._graphItem:GLGraphItem = None
        self._color:list = [1.0, 0.0, 0.0, 1.0]
        self._visible:bool = True
         
    def initTreeItem(self):
        '''
        Create model tree Items.
        创建模型树条目
        '''
        text = self._object.name
        id = str(self._object.id)
        self._treeItem.setText(0, text)
        self._treeItem.setText(1, id)
        
    def initObject(self):
        '''
        Create visual model Entries.
        创建可视化模型对象：
        '''
        pass
    
    def setViewPort(self, viewport:GLViewWidget):
        self._viewport = viewport
        
    def setVisible(self, visible:bool):
        self._visible = visible
        self.graphItem.setVisible(visible)
        
    @property
    def color(self) -> list:
        return self._color
    
    @property
    def graphItem(self) -> GLGraphItem:
        return self._graphItem
    
    @property
    def treeItem(self) -> QTreeWidgetItem:
        return self._treeItem
    
    @property
    def viewport(self) -> GLViewWidget:
        return self._viewport
    
    @property
    def object(self):
        return self._object
    
    @property
    def visible(self) -> bool:
        return self._visible