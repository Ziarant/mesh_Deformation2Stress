import numpy as np
    
def calculate_S3(element) -> np.ndarray:
    
    A = (element.nodes[1].coord[0] *element.nodes[2].coord[1] - \
        element.nodes[2].coord[0] *element.nodes[1].coord[1] + \
        element.nodes[2].coord[0] *element.nodes[0].coord[1] - \
        element.nodes[0].coord[0] *element.nodes[2].coord[1] + \
        element.nodes[0].coord[0] *element.nodes[1].coord[1] - \
        element.nodes[1].coord[0] *element.nodes[0].coord[1])*0.5
    
    tempVal = 0.5 / A
    
    B = np.array([[element.nodes[1].coord[1] -element.nodes[2].coord[1] ,0.0,
                    element.nodes[2].coord[1] -element.nodes[0].coord[1] ,0.0,
                    element.nodes[0].coord[1] -element.nodes[1].coord[1] ,0.0],
                    [0.0,element.nodes[2].coord[0] -element.nodes[1].coord[0] ,
                    0.0,element.nodes[0].coord[0] -element.nodes[2].coord[0] ,
                    0.0,element.nodes[1].coord[0] -element.nodes[0].coord[0] ],
                    [element.nodes[2].coord[0] -element.nodes[1].coord[0] ,
                    element.nodes[1].coord[1] -element.nodes[2].coord[1] ,
                    element.nodes[0].coord[0] -element.nodes[2].coord[0] ,
                    element.nodes[2].coord[1] -element.nodes[0].coord[1] ,
                    element.nodes[1].coord[0] -element.nodes[0].coord[0] ,
                    element.nodes[0].coord[1] -element.nodes[1].coord[1] ]])*tempVal

    return B.T

class BMatrix(object):
    '''
    Calculated B-Matrix of elements.
    '''
    def __init__(self, element):
        self._element = element
        self._matrix = None
        
    def calculate(self):
        elemType = self._element.elemType
        if elemType == 'S3':
            self._matrix = calculate_S3(self._element)

        
    @property
    def matrix(self):
        return self._matrix