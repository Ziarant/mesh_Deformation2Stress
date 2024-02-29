import sys
from abc import ABC, abstractmethod

sys.path.append('..')
from objects.baseMaterial import BaseMaterial

class BaseSection(ABC):
    '''
	Abstract Base Class for sections.
	'''
    
    _nextId = 1
    @abstractmethod
    def __init__(self):
        self._id = BaseSection._nextId
        BaseSection._nextId += 1
        
        self._name = None
        self._material:BaseMaterial = None
        self._data:list = None
        
    def setName(self, name):
        self._name = name
        
    def setData(self, data:list):
        self._data = data
        
    def setMaterial(self, material:BaseMaterial):
        self._material = material
        
    @property
    def id(self):
        return self._id
        
    @property
    def name(self):
        return self._name
    
    @property
    def component(self):
        return self._component
    
    @property
    def material(self):
        return self._material