import sys

sys.path.append("..")
from objects.baseElement import BaseElement, GAUSS_S4

class S4(BaseElement):
    def __init__(self, label:int, sect, nodes:list):
        super().__init__(label, sect, nodes)
        self.setGauss(GAUSS_S4)
        self.setType('S4')
        self.setOrder(1)
        
class S4R(S4):
    def __init__(self, label:int, sect, nodes:list):
        super().__init__(label, sect, nodes)
        self.setGauss(GAUSS_S4)
        self.setType('S4R')
        self.setOrder(1)