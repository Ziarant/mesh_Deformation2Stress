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

            sourceNode.setSolution('U', (x, y, z))
            count += 1
            
        print('The U-field calculation is complete, Total amount of node data written:[%d/%d]'%(count, numSourceNodes))
            
            