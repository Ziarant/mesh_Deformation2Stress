import numpy as np
    
# TODO: Supplementary More Element Type
def calculate_CPS3(element) -> np.ndarray:
    x1, y1 = element.nodes[0].coord[0], element.nodes[0].coord[1]
    x2, y2 = element.nodes[1].coord[0], element.nodes[1].coord[1]
    x3, y3 = element.nodes[2].coord[0], element.nodes[2].coord[1]
    
    # Triangle Element Area:
    A = (x2*y3 - x3*y2 + x3*y1 - x1*y3 + x1*y2 - x2*y1) * 0.5
    
    tempVal = 0.5 / A
    
    # [S] = [N1, N2, N3]        Shape Function matrix:  [3, N]
    # [dS] = [delta][S]         Derivative of Shape Function matrix: [6, 3]·[3, N] -> [6, N]
    # [B] = [dS] / A
    B = np.array([[y2 -y3 , 0.0,    y3 -y1, 0.0,    y1 -y2 ,0.0    ],
                  [0.0,     x3 -x2, 0.0,    x1 -x3, 0.0,    x2 -x1 ],
                  [x3 -x2 , y2 -y3, x1 -x3, y3 -y1, x2 -x1, y1 -y2 ]]) *tempVal

    return B.T

def calculate_S3(element) -> np.ndarray:
    B = calculate_CPS3(element)
    return B

def calculate_S4(element) -> np.ndarray:
    B = calculate_CPS3(element)
    return B
    
class BMatrix(object):
    '''
    Calculated Strain-Displacement-Matrix (B-Matrix) [6, 3] of elements.
    '''
    def __init__(self, element):
        self._element = element
        self._matrix = None
        
    def calculate(self):
        elemType = self._element.elemType
        if elemType == 'CPS3':
            self._matrix = calculate_CPS3(self._element)
            return
        if elemType == 'S3':
            self._matrix = calculate_S3(self._element)
            return
        if elemType == 'S4':
            self._matrix = calculate_S4(self._element)
            return
        if elemType == 'S4R':
            self._matrix = calculate_S4(self._element)
            return
        else:
            self._matrix = calculate_CPS3(self._element)
            return

    @property
    def matrix(self):
        return self._matrix