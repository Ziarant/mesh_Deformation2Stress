# 等参单元形函数
'''
    1-D:
        2节点杆单元：C3D2
            N1 = 1 - x/L
            N2 = x/L
        3节点杆单元：
            N1 = (L^3 - 3Lx^2 + 2x^3) / L^3
            N2 = (L^2x - 2Lx^2 + x^3) / L^2
            N3 = (x^3 - Lx^2) / L^2
    2-D:
        3节点三角形单元：
        6节点三角形单元：
        10节点三角形单元：
        15节点三角形单元：
        4节点四边形单元：
        8节点四边形单元：
        9节点四边形单元：
    3-D:
        4节点四面体单元：
        10节点四面体单元：
        8节点六面体单元：
        14节点六面体单元：
        20节点六面体单元：
'''

import numpy as np
import sympy

def calculate_Rod2(element):
    nodes = element.nodes
    L = nodes[1].coord - nodes[0].coord
    L = np.linalg.norm(L)
    x = sympy.Symbol("x")
    N1 = 1 - x / L
    N2 = x / L
    dN1 = [-1/L, 0, 0]
    dN2 = [1/L, 0, 0]
    return [N1, N2], [dN1, dN2]

def calculate_Rod3(element):
    # TODO: 实现计算3节点杆单元的S矩阵
    pass

def calculate_Tri3(element):
    nodes = element.nodes
    L1 = nodes[1].coord - nodes[0].coord
    L2 = nodes[2].coord - nodes[1].coord
    L3 = nodes[0].coord - nodes[2].coord
    L1 = np.linalg.norm(L1)
    L2 = np.linalg.norm(L2)
    L3 = np.linalg.norm(L3)
    N1 = L1
    N2 = 1- L1 - L2
    N3 = L2
    dN1 = [0, 0, 0]
    dN2 = [0, 0, 0]
    dN3 = [0, 0, 0]
    return [N1, N2, N3], [dN1, dN2, dN3]

def calculate_Tri6(element):
    # TODO: 实现计算6节点三角形单元的S矩阵
    pass

def calculate_Tri10(element):
    # TODO: 实现计算10节点三角形单元的S矩阵
    pass

def calculate_Tri15(element):
    # TODO: 实现计算15节点三角形单元的S矩阵
    pass

def calculate_Quad4(element):
    x, y = sympy.Symbol("x"), sympy.Symbol("y")
    N1 = 0.25 * (1 - x) * (1 - y)
    N2 = 0.25 * (1 - x) * (1 + y)
    N3 = 0.25 * (1 + x) * (1 + y)
    N4 = 0.25 * (1 + x) * (1 - y)
    dN1 = [0.25 * (1 - y), 0.25 * (1 - x), 0]
    dN2 = [0.25 * (1 + y), 0.25 * (1 - x), 0]
    dN3 = [0.25 * (1 + y), 0.25 * (1 + x), 0]
    dN4 = [0.25 * (1 - y), 0.25 * (1 + x), 0]
    return [N1, N2, N3, N4], [dN1, dN2, dN3, dN4]

def calculate_Quad8(element):
    # TODO: 实现计算8节点四边形单元的S矩阵
    pass

class SMatrix(object):
    '''
    Calculated Shape-Function-Matrix (S-Matrix) [3, 3 * N] of elements.
    [S] = [N1, N2, ……, Nn]
    '''
    def __init__(self, element):
        self._element = element
        self._matrix = None
        self._NDiff = None
        
    def calculate(self):
        elemType = self._element.elemType
        if elemType in ['C3T2']:
            self._matrix, self._NDiff = calculate_Rod2(self._element)
        elif elemType in ['CPS3', 'S3']:
            self._matrix, self._NDiff = calculate_Tri3(self._element)
        elif elemType in ['S4', 'S4R']:
            self._matrix, self._NDiff = calculate_Quad4(self._element)    
            
    @property
    def matrix(self):
        return self._matrix
    
    @property
    def NDiff(self):
        return self._NDiff