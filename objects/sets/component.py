import sys

sys.path.append("..")
from objects.baseSet import BaseSet
from objects.baseSection import BaseSection

class Component(BaseSet):
    _instances = {}
    
    def __init__(self, name):
        super().__init__()
        self.setName(name)
        self.setType('ELSET')
        
    def __new__(cls, name:str):
        '''
        If an instance with the same name already exists,   
        the existing instance is returned instead of creating a new one.
        '''
        if name in cls._instances.keys():
            return cls._instances[name]
        else:
            instance = super().__new__(cls)
            cls._instances[name] = instance
            return instance