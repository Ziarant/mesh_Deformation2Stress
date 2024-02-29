from PyQt5.QtWidgets import QTreeWidgetItem


class BaseHandle(object):
    def __init__(self):
        self._object = None
        self._treeItem = QTreeWidgetItem()
         
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
        创建可视化模型对象
        '''
        pass
    
    @property
    def treeItem(self) -> QTreeWidgetItem:
        return self._treeItem