import sys

sys.path.append('..')

from conversion.loader import BaseLoader
from objects.nodes import Node
from objects.baseElement import ELEMENTTYPELIST, BaseElement
from objects.elements import *

class Parser():
    def __init__(self, loader:BaseLoader):
        self._loader = loader
        
        self._nodesMap:map = None
        self._elementsMap:map = None
        self._nodesDict:dict = {}
        
        self.instantiate()
        
    def instantiate(self):
        self.instantiateNodes()
        self.instantiateElements()
        
    def instantiateNodes(self):
        isinstiateNode = lambda x : Node(x[0], x[1], x[2], x[3])
        
        nodes = self._loader.nodes
        self._nodesMap:map = map(isinstiateNode, nodes)
        self._nodesList:list = list(self._nodesMap)
        self.nodesLabelMap()
        
    def nodesLabelMap(self):
        '''
        Create a mapping between labels and nodes.
        '''
        for node in self._nodesList:
            self._nodesDict[str(node.label)] = node
        
    def instiateElement(self, elementInfo) -> BaseElement:
        elemType = elementInfo[0]
        label = elementInfo[1]
        sect = elementInfo[2]
        nodesIndexList:list = elementInfo[3]
        nodes:list = []
        for label in nodesIndexList:
            nodes.append(self._nodesDict[str(label)])
        return globals()[elemType](label, sect, nodes)
        
    def instantiateElements(self):
        elementsDict = self._loader.elements
        elements:list = []
        for elemType in elementsDict.keys():
            if elemType not in ELEMENTTYPELIST:
                continue
            for sect in elementsDict[elemType].keys():
                elementInfos:list = elementsDict[elemType][sect]
                for elementInfo in elementInfos:
                    label = elementInfo[0]
                    nodes = elementInfo[1:]
                    elements.append([elemType, label, sect, nodes])
                
        self._elementsMap:map = map(self.instiateElement, elements)
        self._elementsList:list = list(self._elementsMap)
        
    @property
    def nodes(self) -> list:
        return self._nodesList
    
    @property
    def elements(self) -> list:
        return self._elementsList
        