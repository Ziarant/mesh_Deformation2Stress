import sys
import numpy as np

sys.path.append('..')

from .baseField import BaseField
from _parser.parser import Parser

class EField(BaseField):
    '''
    Based on the node `coord` and `U` of the source and the target mesh,
    the element strain is calculated and written in element objects.
    '''
    def __init__(self, source:Parser, target:Parser):
        super().__init__()
        self.setName('E')
        self.setType('TENSOR_3D_PLANER')
        self.setPosition('INTEGRATION_POINT')
        
        self._sourceElements:list = source.elements
        
        self.cal_EField()
        
    def cal_EField(self):
        '''
        Calculate and Write `Strain` data to elements
        '''
        for element in self._sourceElements:
            element.calculate_Strain()
        
    
