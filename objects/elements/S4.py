import sys
import numpy as np

sys.path.append("..")
from objects.baseElement import BaseElement, GAUSS_S4
from objects.sets.component import Component

class S4(BaseElement):
    def __init__(self, label:int, elSet:str, nodes:list):
        super().__init__()
        self.setGauss(GAUSS_S4)
        self.setType('S4')
        self.setGaussWidget(1)
        self.setOrder(1)
        
        self._label = label
        component = Component(elSet)
        self.setComponent(component)
        self.setNodes(nodes)
        self.set3D(False)
        self.setGaussPoints(self.gauss)
        
        
class S4R(S4):
    def __init__(self, label:int, elSet:str, nodes:list):
        super().__init__(label, elSet, nodes)
        self.setType('S4R')
        self.set3D(False)