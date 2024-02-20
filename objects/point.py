import numpy as np

class Point(object):
    _nextId = 1
    
    def __init__(self, x:float=0, y:float=0, z:float=0):
        self.id = Point._nextId
        Point._nextId += 1
        
        self._x:float = x
        self._y:float = y
        self._z:float = z
        
        self._coord = [self.x, self.y, self.z]
        
    @property
    def x(self) -> float:
        return self._x
    
    @property
    def y(self) -> float:
        return self._y
    
    @property
    def z(self) -> float:
        return self._z