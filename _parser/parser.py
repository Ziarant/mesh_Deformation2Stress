import sys

sys.path.append('..')

from conversion.loader import BaseLoader
from objects.nodes import Node
from objects.baseElement import ELEMENTTYPELIST, BaseElement
from objects.elements import *
from objects.baseMaterial import BaseMaterial
from objects.materials import *
from objects.baseSection import BaseSection
from objects.sections import *

class Parser(object):
    '''
    Parse data.
    If not the source data, could set `isSource = False` to reduce computation complexity.
    '''
    def __init__(self, loader:BaseLoader, isSource:bool = True):
        self._loader = loader
        
        self._nodesMap:map = None
        self._elementsMap:map = None
        self._nodesList:list = None
        self._elementsList:list = None
        self._nodesDict:dict = {}
        self._materials:dict = {}
        self._sections:dict = {}
        
        self.instantiate(isSource)
        
    def instantiate(self, isSource:bool = True):
        self.instantiateNodes()
        if isSource:
            self.instantiateMaterials()
            self.instantiateElements()
            self.instantiateSections()
        
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
        
    def instiateElement(self, elementInfo:list) -> BaseElement:
        elemType = elementInfo[0]
        label = elementInfo[1]
        elemSet = elementInfo[2]
        nodesIndexList:list = elementInfo[3]
        nodes:list = []
        for label in nodesIndexList:
            nodes.append(self._nodesDict[str(label)])
        if elemType not in globals().keys():
            return None
        return globals()[elemType](label, elemSet, nodes)
        
    def instantiateElements(self):
        elementsDict = self._loader.elements
        elements:list = []
        for elemType in elementsDict.keys():
            elemType = elemType.upper()
            if elemType not in ELEMENTTYPELIST:
                continue
            for elemSet in elementsDict[elemType].keys():
                elementInfos:list = elementsDict[elemType][elemSet]
                for elementInfo in elementInfos:
                    label = elementInfo[0]
                    nodes = elementInfo[1:]
                    elements.append([elemType, label, elemSet, nodes])
                
        self._elementsMap:map = map(self.instiateElement, elements)
        self._elementsList:list = list(self._elementsMap)
        
    def instantiateMaterial(self, matInfo:list) -> BaseMaterial:
        matName, matType, matData = matInfo[0], matInfo[1], matInfo[2]
        matType = matType.upper()
        if matType not in globals().keys():
            print('%s is not a known material type'%matType)
            return None
        material = globals()[matType](matName, matData)
        return material
        
    def instantiateMaterials(self):
        for matName in self._loader.materials.keys():
            matType = self._loader.materials[matName][0]
            matData = self._loader.materials[matName][1]
            material = self.instantiateMaterial([matName, matType, matData])
            if material is None:
                continue
            self._materials[matName] = material
            
    def instantiateSection(self, sectionInfo:list) -> BaseSection:
        sectionType, elsetName = sectionInfo[0], sectionInfo[1]
        matName, sectionData = sectionInfo[2], sectionInfo[3]
        sectionType = sectionType.upper()
        if sectionType not in globals().keys():
            return None
        return globals()[sectionType](elsetName, matName, sectionData)
            
    def instantiateSections(self):
        for section in self._loader.sections.keys():
            sectionType = self._loader.sections[section][0]
            elsetName = self._loader.sections[section][1]
            matName = self._loader.sections[section][2]
            sectionData = self._loader.sections[section][3]
            section = self.instantiateSection([sectionType, elsetName, matName, sectionData])
            if section is None:
                continue
            self._sections[elsetName] = section
            
    @property
    def nodes(self) -> list:
        return self._nodesList
    
    @property
    def elements(self) -> list:
        return self._elementsList
    
    @property
    def materials(self) -> dict:
        return self._materials
        