import numpy as np

class Node(object):
    '''
    Base class for nodes.
    '''
    _nextId = 1
    def __init__(self, label:int, x:float, y:float, z:float=0.0, part:object = None):
        self._id = Node._nextId
        Node._nextId += 1
        
        self._label = label
        self._x = x
        self._y = y
        self._z = z
        self._coord = [self.x, self.y, self.z]
        self._NFS = [0,0,0,0,0,0]
        self._solutions = {}
        self._elements = {}
        self._part:object = part
        
        # Properties
        self._isOnSurface = False
        
    def translate(self, x:float, y:float, z:float=0.0):
        self._x += x
        self._y += y
        self._z += z
        
    def setCoord(self, x:float, y:float, z:float=0.0):
        self._x = x
        self._y = y
        self._z = z
        return self.coord
    
    def setPart(self, part:object):
        self._part = part
    
    def appendElement(self, element):
        self._elements[element.id] = element
    
    def getSolution(self, key:str):
        if key in self._solutions:
            return self._solutions[key]
        
    def setSolution(self, key:str, value):
        valueTypeName = type(value).__name__        
        if valueTypeName == 'dict':
            if key not in self._solutions.keys():
                self._solutions[key] = {}
            for valuekey in value.keys():
                self._solutions[key][valuekey] = value[valuekey]
            return
        else:
            self._solutions[key] = value
            
    def print(self, key:str):
        '''
        Print data to TERMINAL
        '''
        if key not in self._solutions.keys():
            return
        solution = self._solutions[key]
        output = 'Node label:{} \t {} \t value: \t{}'.format(self.label, key, solution)
        print(output)
        
    @property
    def id(self) -> int:
        return self._id
        
    @property
    def label(self) -> int:
        return self._label
    
    @property
    def x(self) -> float:
        return self._x
    
    @property
    def y(self) -> float:
        return self._y
    
    @property
    def z(self) -> float:
        return self._z
    
    @property
    def coord(self) -> list:
        return np.array(self._coord)
    
    @property
    def elements(self) -> dict:
        return self._elements
    
    @property
    def NFS(self) -> list:
        return self._NFS
    
    @property
    def part(self) -> object:
        return self._part
    
    @property
    def solutions(self) -> dict:
        return self._solutions
    
    @property
    def isOnSurface(self) -> bool:
        '''
        Surface Node: True or False
        '''
        return self._isOnSurface
