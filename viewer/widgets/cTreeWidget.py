from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem
class CTreeWidget(QTreeWidget):
    def __init__(self, parent:QWidget=None):
        super().__init__(parent)
        
        self.setColumnCount(3)
        self.init()
        
    def init(self):
        self.setHeaderLabels(['Name', 'id', 'Color'])
        self.setColumnWidth(0, 150)
        self.setColumnWidth(1, 60)
        self.setColumnWidth(2, 60)
        
        self._rootItems:list = []
        self._componentRootItem = QTreeWidgetItem(self)
        self._componentRootItem.setText(0, 'Components')
        self._componentRootItem.setHidden(True)
        self.rootItems.append(self._componentRootItem)
        
    def updateRootItems(self):
        for rootItem in self.rootItems:
            if rootItem.childCount() > 0:
                rootItem.setHidden(False)
                rootItem.setExpanded(True)
            else:
                rootItem.setHidden(True)

    @property
    def componentRootItem(self) -> QTreeWidgetItem:
        return self._componentRootItem
    
    @property
    def rootItems(self) -> list:
        return self._rootItems
        

