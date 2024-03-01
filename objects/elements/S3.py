import sys
import numpy as np

sys.path.append("..")
from objects.baseElement import BaseElement, GAUSS_S3
from objects.sets.component import Component

class CPS3(BaseElement):
    '''
    Class for triangular 3-node 2D element(constant strain triangle element).
    The element has three nodes, each with two degrees of freedom.
    '''
    def __init__(self, label:int, elSet:str, nodes:list):
        super().__init__()
        self.setGauss(GAUSS_S3)
        self.setType('CPS3')
        self.setOrder(1)
        self.set3D(False)
        
        self._label = label
        component = Component(elSet)
        self.setComponent(component)
        self.setNodes(nodes)
        
        self.setGaussPoints(self.gauss)
        

class S3(BaseElement):
    '''
    Class for triangular 3-node 3D element(constant strain triangle element).
    The element has three nodes, each with 3 degrees of freedom
    '''
    def __init__(self, label:int, elSet:str, nodes:list):
        super().__init__()
        self.setGauss(GAUSS_S3)
        self.setGaussWidget(1.0 / 2)
        self.setType('S3')
        self.setOrder(1)
        self.set3D(False)
        
        self._label = label
        component = Component(elSet)
        self.setComponent(component)
        self.setNodes(nodes)

        self.setGaussPoints(self.gauss)
        self.initShape()
        
    def initShape(self):
        nodes = self.nodes
        self._vertexes = np.array([nodes[0].coord, nodes[1].coord, nodes[2].coord])
        self._faces = np.array([[0, 1, 2]])
        self._edges = np.array([[0, 1], [1, 2], [2, 0]])