import sys
from abc import ABC, abstractmethod

sys.path.append('..')
from objects.baseSection import BaseSection
from objects.baseMaterial import BaseMaterial

TYPE = ['ELSET', 'NSET', 'SURFACE_NODE', 'SURFACE_ELEMENT']
class BaseSet(ABC):
    '''
    Abstract Base Class for sets.
    '''
    
    _nextId = 1
    @abstractmethod
    def __init__(self):
        self._id = BaseSet._nextId
        BaseSet._nextId += 1
        
        self._name:str = None
        self._section:BaseSection = None
        
        # Set Type
        self._isELSET:bool = False
        self._isNSET:bool = False
        self._isSURFACE_NODE:bool = False
        self._isSURFACE_ELEMENT:bool = False
        
    def setName(self, name:str):
        self._name = name
        
    def setType(self, _type:str):
        self._isELSET:bool = False
        self._isNSET:bool = False
        self._isSURFACE_NODE:bool = False
        self._isSURFACE_ELEMENT:bool = False
        if _type in TYPE:
            if _type == 'ELSET':
                self._isELSET = True
            elif _type == 'NSET':
                self._isNSET = True
            elif _type == 'SURFACE_NODE':
                self._isSURFACE_NODE = True
            elif _type == 'SURFACE_ELEMENT':
                self._isSURFACE_ELEMENT = True
                
    def setSection(self, section:BaseSection):
        self._section = section
        
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def type(self):
        return self._type
    
    @property
    def isELSET(self):
        return self._isELSET
    
    @property
    def isNSET(self):
        return self._isNSET
    
    @property
    def isSURFACE_NODE(self):
        return self._isSURFACE_NODE
    
    @property
    def isSURFACE_ELEMENT(self):
        return self._isSURFACE_ELEMENT
    
    @property
    def section(self):
        return self._section
    
    @property
    def material(self):
        return self._section.material
    