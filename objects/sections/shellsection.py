import sys

sys.path.append("..")
from objects.baseSection import BaseSection
from objects.baseMaterial import BaseMaterial
from objects.sets.component import Component

class SHELLSECTION(BaseSection):
    
    _nextId = 1
    def __init__(self, compName:str, matName:str, sectionData:list):
        self.setName(compName)
        _material = BaseMaterial.call(matName)
        self.setMaterial(_material)
        self.setData(sectionData)
        
        self._id = SHELLSECTION._nextId
        SHELLSECTION._nextId += 1
        
        component = Component(compName)
        component.setSection(self)