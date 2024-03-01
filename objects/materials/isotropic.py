import sys

sys.path.append("..")
from objects.baseMaterial import BaseMaterial

class ISOTROPIC(BaseMaterial):
    '''
    Isotropic Linear Elastic Material
    '''
    def __init__(self, name:str, data:list):
        if name not in BaseMaterial._instances.keys():
            BaseMaterial._instances[name] = self
        
        super().__init__()
        
        self.setName(name)
        self._data = data

        self.parse()
        
    def parse(self):
        nData = len(self.data)
        self._elastMod:float = self.data[0]
        self._poisson:float = self.data[1]
        self._density:float = self.data[2] if nData > 2 else 0.0
        self._shearMod:float = self.E / (2*(1-self.nu))
        self.calElasticTensor()
    
    @property
    def data(self):
        return self._data