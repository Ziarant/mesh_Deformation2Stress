import numpy as np

class SMatrix(object):
    '''
    Calculated Shape-Function-Matrix (S-Matrix) [3, 3 * N] of elements.
    [S] = [N1, N2, ……, Nn]
    '''
    def __init__(self, element):
        self._element = element