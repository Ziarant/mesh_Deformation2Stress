import sys
import numpy as np

sys.path.append('..')

from .baseField import BaseField
from _parser.parser import Parser

class SField(BaseField):
    def __init__(self, source:Parser):
        super().__init__()
        self.setName('E')
        self.setType('TENSOR_3D_PLANER')
        self.setPosition('INTEGRATION_POINT')
        
        self._sourceNodes:list = source.nodes
        self._sourceElements:list = source.elements
        
        self.cal_SField()
        
    def cal_SField(self):
        '''
        Calculate and Write `Stress` data to elements
        '''
        for element in self._sourceElements:
            element.calculate_Stress()
            
        for node in self._sourceNodes:
            node_S_Tensor = []
            for elemLabel in node.elements.keys():
                elem = node.elements[elemLabel]
                node_S_Tensor.append(elem.getSolution('S_Tensor'))
                
            node_S_Tensor = np.array(node_S_Tensor)
            node_S_Mean = np.mean(node_S_Tensor, axis=0)
            if np.isnan(node_S_Mean).any():
                node.setSolution('S_Tensor', [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan])
                continue
            
            node.setSolution('S_Tensor', node_S_Mean)
            
    def print(self):
        '''
        Print the S-field data to TERMINAL.
        '''
        for sourceNode in self._sourceNodes:
            if 'S_Tensor' not in sourceNode.solutions.keys():
                continue
            S = sourceNode.getSolution('S_Tensor')
            output = 'Node label:{} \t S_Tensor:\t{:.3e}, {:.3e}, {:.3e}, {:.3e}, {:.3e}, {:.3e}'.format(sourceNode.label, *S)
            print(output)
            