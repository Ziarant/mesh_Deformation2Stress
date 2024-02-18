# Computes the Jacobian matrix on the node based on the cell type and node coordinates.
# 基于单元类型和节点坐标计算节点上的雅可比矩阵
'''
    雅可比矩阵描述了从全局坐标系到参考坐标系（通常是单元的局部坐标系）的坐标变换。
    对于非等参单元，雅可比矩阵在每个节点上可能是不一致的。
    - 因此需要在每个节点上进行单独的计算，以考虑形函数的定义域的变化。
    非等参单元的雅可比矩阵需要根据非等参单元的具体形函数进行计算：
    - 在每个节点上，通过将形函数对参考坐标的偏导数进行求解，可以得到相应的雅可比矩阵。
'''

import numpy as np

def calculate_S3(element):
    '''
    Calculate Jacobi-Matrix of S3 element.
    [J]:
    '''
    NDIFF = element.S_Matrix.NDiff
    J = np.zeros((3, 3))

    return J

class JMatrix(object):
    '''
    Calculated Jacobi-Matrix of elements.
    [J]: 
    '''
    def __init__(self, element):
        self._element = element
        self._matrix = None

    def calculate(self):
        elemType = self._element.elemType
        if elemType == 'S3':
            self._matrix = calculate_S3(self._element)
            return
        
    @property
    def matrix(self):
        return self._matrix