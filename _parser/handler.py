import sys
from PyQt5.QtWidgets import QTreeWidget
from pyqtgraph.opengl.GLViewWidget import GLViewWidget

sys.path.append('..')
from _parser.parser import Parser
from viewer.handles import *

class Handler(object):
    '''
    Transform <Parse-objects> to <Handle-objects>.  
    将解析对象转化为可视化句柄对象
    '''
    def __init__(self, parser:Parser, viewport:GLViewWidget = None):
        self._name = None
        self._parser = parser
        
        self._treeWidget:QTreeWidget = None
        self._viewport:GLViewWidget = viewport
        
        self._nodes = self._parser.nodes
        self._elements = self._parser.elements
        self._materials = self._parser.materials
        self._sections = self._parser.sections
        
        self._nodeHandles:list = []
        self._elementHandles:list = []
        self._materialHandles:dict = {}
        self._componentHandle:dict = {}
        
        self.transform()
        
    def transform(self):
        for node in self._nodes:
            self._nodeHandles.append(NodeHandle(node, self.viewport))
            
        for element in self._elements:
            self._elementHandles.append(ElementHandle(element, self.viewport))
            
        for materialName in self._materials.keys():
            self._materialHandles[materialName] = MaterialHandle(self._materials[materialName])

        for sectionName in self._sections.keys():
            self._componentHandle[sectionName] = ComponentHandle(self._sections[sectionName], self.viewport)
            
    def setName(self, name:str):
        self._name = name
        
    def setTreeWidget(self, treeWidget:QTreeWidget):
        self._treeWidget = treeWidget
        
    def updateItems(self):
        # 添加Component
        for compName in self._componentHandle.keys():
            compHandle = self._componentHandle[compName]
            compTreeItem = compHandle.treeItem
            self.treeWidget.componentRootItem.addChild(compTreeItem)
            
        self.treeWidget.updateRootItems()
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def nodeHandles(self) -> list:
        return self._nodeHandles
    
    @property
    def elementHandles(self) -> list:
        return self._elementHandles
    
    @property
    def materialHandles(self) -> dict:
        return self._materialHandles
    
    @property
    def componentHandle(self) -> dict:
        return self._componentHandle
    
    @property
    def treeWidget(self) -> QTreeWidget:
        return self._treeWidget
    
    @property
    def viewport(self) -> GLViewWidget:
        return self._viewport