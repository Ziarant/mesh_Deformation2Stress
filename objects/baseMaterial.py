from abc import ABC, abstractmethod
import numpy as np

class BaseMaterial(ABC):
    '''
	Abstract Base Class for materials.
	'''
    _nextId = 1
    _instances = {}
    
    @abstractmethod
    def __init__(self):
        self._id = BaseMaterial._nextId
        BaseMaterial._nextId += 1
        
        self._name = None
        self._isIsotropic:bool = True
        self._is3D:bool = True
        self._isPlate:bool = False
        self._elastMod = None
        self._elastTensor = None
        self._poisson = None
        self._density = None
        self._shearMod = None
        
    @classmethod
    def call(cls, name):
        if name in cls._instances.keys():
            return cls._instances[name]
        else:
            print('%s is not Exists'%name)
            return None
        
    def setName(self, name:str):
        self._name = name
        
    def setIsotropic(self, isotropic:bool):
        self._isIsotropic = isotropic
        
    def set3D(self, is3D:bool):
        self._is3D = is3D
        
    def setPlate(self, isPlate:bool):
        self._isPlate = isPlate
        
    def setElasticTensor(self, elasticTensor:np.ndarray):
        self._elastTensor = elasticTensor
        
    def calElasticTensor(self):
        '''
        Calculate the elastic tensor of the section.
        '''
        E = self._elastMod
        v = self._poisson
        if not self.isIsotropic:
            return
        if self.is3D:
            if self.isPlate:
                _elasticTensor = np.array([ [E/(1-v**2), (v*E)/(1-v**2), 0, 0, 0, 0],
                                            [(v*E)/(1-v**2), E/(1-v**2), 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0],
                                            [ 0, 0, 0, (0.5*(1-v)*E)/(1-v**2), 0, 0],
                                            [0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0]])
            else:
                XE = E/((1+v)*(1-(2*v)))
                _elasticTensor = np.array([ [ XE*(1-v), 	XE*v,      0,       0,          0,      0],
                                            [ XE*v,         XE*(1-v),  0,       0,          0,      0],
                                            [ 0,            0,         0,       0,          0,      0],
                                            [ 0,            0,         0,       XE*(1-2*v), 0,      0],
                                            [ 0,            0,         0,       0,          0,      0],
                                            [ 0,            0,         0,       0,          0,      0]])
        else:
            XE = E/((1+v)*(1-2*v))
            _elasticTensor = np.array([ [XE*(1-v),  XE*v,       XE*v,       0,          0,          0],
                                        [XE*v,      XE*(1-v),   XE*v,       0,          0,          0],
                                        [XE*v,      XE*v,       XE*(1-v),   0,          0,          0],
                                        [0,         0,          0,          XE*(0.5-v), 0,          0],
                                        [0,         0,          0,          0,          XE*(0.5-v), 0],
                                        [0,         0,          0,          0,          0,          XE*(0.5-v)]])
        self.setElasticTensor(_elasticTensor)
        
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def isIsotropic(self):
        return self._isIsotropic
    
    @property
    def is3D(self):
        return self._is3D
    
    @property
    def isPlate(self):
        return self._isPlate
    
    @property
    def E(self) -> float:
        '''
        Elastic Modulus.
        '''
        return self._elastMod
    
    @property
    def elasticTensor(self) -> np.ndarray:
        '''
        Elastic Tensor[6, 6].
        '''
        return self._elastTensor
    
    @property
    def nu(self):
        '''
        Possion ratio.
        '''
        return self._poisson