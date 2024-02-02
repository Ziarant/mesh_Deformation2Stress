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
        
        self._sourceElements:list = source.elements
        
        self.cal_SField()
        
    def cal_SField(self):
        '''
        Calculate and Write `Stress` data to elements
        '''
        for element in self._sourceElements:
            element.calculate_Stress()