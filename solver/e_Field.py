import sys
import numpy as np
import sympy

sys.path.append('..')

from .baseField import BaseField
from _parser.parser import Parser

class EField(BaseField):
    '''
    Based on the node `coord` and `U` of the source and the target mesh,
    the element strain is calculated and written in element objects.
    '''
    def __init__(self, source:Parser):
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
            
    def print(self):
        '''
        Print the E_Tensor data to TERMINAL.
        '''
        count = 0
        for element in self._sourceElements:
            # if 'E_Tensor' in element.solutions.keys():
            #     E = element.getSolution('E_Tensor')
            #     output = 'Elem label:{} \t E_Tensor:\t{:.3e}, {:.3e}, {:.3e}, {:.3e}, {:.3e}, {:.3e}'.format(element.label, *E)
            #     print(output)
            #     count += 1
            
            # TEST:测试输出——形函数
            F = element.S_Matrix
            v = F[0]
            if type(v).__name__ == 'Mul':
                # 局部坐标求解：
                xi, eta, zeta = sympy.symbols('xi, eta, zeta')
                S = []
                for f in F:
                    solve = f.subs({xi:0, eta:0, zeta:0})
                    S.append(solve)
                print(S)
                
        if count == 0:
            print('Warning: No E_Tensor data found.')
        
    
