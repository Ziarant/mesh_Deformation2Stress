import sys
import numpy as np

sys.path.append('..')

from .baseField import BaseField
from _parser.parser import Parser
from objects.nodes import Node

class UField(BaseField):
    '''
    Based on the node coordinates of the source and the target mesh,
    the node displacement is calculated and written in node objects.
    '''
    def __init__(self, source:Parser, target:Parser):
        super().__init__()
        self.setName('U')
        self.setType('VECTOR')
        self.setPosition('NODAL')
        
        self._sourceNodes:list = source.nodes
        self._targetNodes:list = target.nodes
        self._correspondences:list = []
        
        self.mapNodes()
        self.cal_UField()
        
    def mapNodes(self):
        count = 0
        for sourceNode in self._sourceNodes:
            label:str = sourceNode.label
            for targetNode in self._targetNodes:
                if targetNode.label == label:
                    self._correspondences.append([label, sourceNode, targetNode])
                    count += 1
                    break

    def cal_UField(self):
        '''
        Write 'U' data to nodes
        '''
        numSourceNodes = len(self._sourceNodes)
        count = 0
        for i in range(len(self._correspondences)):
            correspondence = self._correspondences[i]
            sourceNode:Node = correspondence[1]
            targetNode:Node = correspondence[2]
            
            if isinstance(sourceNode, Node) == False or isinstance(targetNode, Node) == False:
                continue

            x = targetNode.x - sourceNode.x
            y = targetNode.y - sourceNode.y
            z = targetNode.z - sourceNode.z
            
            magnitude = np.sqrt(x**2 + y**2 + z**2)

            sourceNode.setSolution('U', (x, y, z))
            sourceNode.setSolution('U_MAGNITUDE', magnitude)
            count += 1
            
        print('The U-field calculation is complete, Total amount of node data written:[%d/%d]'%(count, numSourceNodes))
       
    def print(self):
        '''
        Print the U-field data to TERMINAL.
        '''
        for sourceNode in self._sourceNodes:
            # sourceNode.print('U')
            # sourceNode.print('U_MAGNITUDE')
            if 'U' not in sourceNode.solutions.keys():
                continue
            U = sourceNode.getSolution('U')
            U_MAGNITUDE = sourceNode.getSolution('U_MAGNITUDE')
            output = 'Node label:{} \t U:\t{:.3f},{:.3f},{:.3f} \t Magnitude:\t{:.3f}'.format(sourceNode.label, *U, U_MAGNITUDE)
            print(output)   
            