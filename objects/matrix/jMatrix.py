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
import sympy

def calculate_Jacobi(element):
    '''
    Calculate Jacobi-Matrix of element.
    [J]:
    '''
    F = element.S_Matrix
    xi, eta, zeta = sympy.symbols('xi, eta, zeta')
    xcoord, ycoord, zcoord = zip(*[node.coord for node in element.nodes])
        
    # TODO: 计算高斯积分点的雅可比矩阵
    n = len(F)
    nGaussPoint = len(element.gaussPoints)
    gPnt = np.zeros((nGaussPoint, 3))
    # 根据形函数计算各高斯积分点的空间坐标：
    for idx_GP in range(nGaussPoint):
        xc = element.gaussPoints[idx_GP][0]
        yc = element.gaussPoints[idx_GP][1]
        zc = element.gaussPoints[idx_GP][2] if len(element.gaussPoints[idx_GP]) > 2 else 0
        
        gPnt[idx_GP][0] = sum(F[i].subs({xi:xc, eta:yc, zeta:zc}) * xcoord[i] for i in range(n))    # x
        gPnt[idx_GP][1] = sum(F[i].subs({xi:xc, eta:yc, zeta:zc}) * ycoord[i] for i in range(n))    # y
        gPnt[idx_GP][2] = sum(F[i].subs({xi:xc, eta:yc, zeta:zc}) * zcoord[i] for i in range(n))    # z
    
    # 根据形函数偏导计算高斯点处的雅可比矩阵
    NDiff = element.NDiff
    J = np.zeros((nGaussPoint, 3, 3))
    for idx_GP in range(nGaussPoint):
        xc = element.gaussPoints[idx_GP][0]
        yc = element.gaussPoints[idx_GP][1]
        zc = element.gaussPoints[idx_GP][2] if len(element.gaussPoints[idx_GP]) > 2 else 0 
        J[idx_GP, :, :] = np.ones((3, 3))
        for i in range(3):
            for j in range(3):
                # 第idx_GP个高斯点的雅可比矩阵 dXj_dUi：
                try:
                    J[idx_GP, i, j] = sum(NDiff[k][i].subs({xi:xc, eta:yc, zeta:zc}) * gPnt[idx_GP][j] for k in range(n))
                except:
                    J[idx_GP, i, j] = sum(NDiff[k][i] * gPnt[idx_GP][j] for k in range(n))

    # print(J[0])
    return np.array(J).astype(float)

def calculate_JacobianRatio(J):
    '''
    计算雅可比率:
    2范数对应体积变化率
    '''
    nJ = len(J)
    normJ = np.zeros(nJ)
    for i in range(nJ):
        normJ[i] = np.linalg.norm(J[i])
        
    maxNorm = np.max(normJ)
    meanNorm = np.mean(normJ)
    minNorm = np.min(normJ)
    if maxNorm == 0:
        return 1.0
    return minNorm / meanNorm

class JMatrix(object):
    '''
    Calculated Jacobi-Matrix of elements.
    [J]: 
    '''
    def __init__(self, element):
        self._element = element
        self._matrix = np.zeros((3, 3))
        self._jacobian = 0.0

    def calculate(self):
        self._matrix = calculate_Jacobi(self._element)
        # 计算雅可比率(高斯点)：
        if len(self._matrix) == 1:
            self._jacobian = 1.0
        else:
            self._jacobian = calculate_JacobianRatio(self._matrix)
        
    @property
    def matrix(self):
        return self._matrix
    
    @property
    def jacobian(self):
        return self._jacobian