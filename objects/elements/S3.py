import sys
import numpy as np

sys.path.append("..")
from objects.baseElement import BaseElement, GAUSS_S3

class S3(BaseElement):
    '''
    Class for triangular 3-node element(constant strain triangle element).
    '''
    def __init__(self, label:int, sect, nodes:list):
        super().__init__(label, sect, nodes)
        self.setGauss(GAUSS_S3)
        self.setType('S3')
        self.setOrder(1)
        self._shapeFunction = None
        
    def updateFreedomSignature(self):
        '''
        Update node freedom signature for nodes in element.
        '''
        for node in self.nodes:
            if node.NFS[0] == 0:
                node.NFS[0] = 1
            if node.NFS[1] == 0:
                node.NFS[1] = 1
      
    def calculate_Strain_Nodal(self):
        '''
        Calculate the strain tensor on nodes.
        '''
        self.calculate_B_Matrix()
        for node in self.nodes:
            U = node.getSolution('U')
            strain_tensor = np.dot(self.B_Matrix, U)
            node.setSolution('E_Tensor_Nodal', {str(self.label) : strain_tensor})
            self.setSolution('E_Tensor_Nodal', {str(node.label) : strain_tensor})
            
    def calculate_Strain(self,
                         averageMethod:str = 'Advanced',
                         averageVariation:float = 75,
                         useCornerData:bool = True):
        '''
        Calculated Strain tensor of element based on the 'E_Tensor_Nodal'.
        ## input
        - ### averageMethod:
            - 'None':
            - 'Advanced':
            - 'Simple':
        ### averageVariation:
        ### useCornerData:
        '''
        if not self.check_nodes_has_U_Data():
            return
        self.calculate_Strain_Nodal()
        strain_tensor = np.zeros((3, 6))
        for i in range(3):
            node = self.nodes[i]
            E_Tensor_Nodal = node.getSolution('E_Tensor_Nodal')
            strain_tensor[i] = E_Tensor_Nodal[str(self.label)]
            
        E_Tensor = strain_tensor.mean(axis=0)
        E_11, E_22, E_33, E_12, E_13, E_23 = E_Tensor[0], E_Tensor[1], E_Tensor[2], E_Tensor[3], E_Tensor[4], E_Tensor[5]
        self.setSolution('E_Tensor', E_Tensor)
        self.setSolution('E', {'E_11' : E_11,
                               'E_22' : E_22,
                               'E_33' : E_33,
                               'E_12' : E_12,
                               'E_13' : E_13,
                               'E_23' : E_23})