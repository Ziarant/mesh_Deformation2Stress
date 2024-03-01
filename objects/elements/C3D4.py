import sys
import numpy as np

sys.path.append("..")
from objects.baseElement import BaseElement, GAUSS_S4
from objects.sets.component import Component

class C3D4(BaseElement):
    def __init__(self, label:int, elSet:str, nodes:list):
        super().__init__()
        self.setGauss(GAUSS_S4)
        self.setType('C3D4')
        self.setGaussWidget(1)
        self.setOrder(1)
        
        self._label = label
        component = Component(elSet)
        self.setComponent(component)
        self.setNodes(nodes)
        self.set3D(True)
        self.setGaussPoints(self.gauss)
        self.initShape()
        
    def initShape(self):
        nodes = self.nodes
        self._vertexes = np.array([nodes[0].coord, nodes[1].coord, nodes[2].coord, nodes[3].coord])
        self._faces = np.array([[0, 1, 2],[0, 1, 3], [2, 3, 0], [1, 2, 3]])
        self._edges = np.array([[0, 1], [1, 2], [2, 3], [3, 0], [0, 2], [1, 3]])