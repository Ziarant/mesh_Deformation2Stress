import sys

sys.path.append("..")
from objects.baseMaterial import BaseMaterial

class ISOTROPIC(BaseMaterial):
    def __init__(self, name:str, data:list):
        if name not in BaseMaterial._instances.keys():
            BaseMaterial._instances[name] = self
        
        super().__init__()
        
        self.setName(name)
        self._data = data

        self.parse()
        
    def parse(self):
        self._elastMod:float = self._data[0]
        self._poisson:float = self._data[1]
        self._density:float = self._data[2]
        self._shearMod:float = self.E / (2*(1-self.nu))
        self.calElasticTensor()
    
    @property
    def data(self):
        return self._data