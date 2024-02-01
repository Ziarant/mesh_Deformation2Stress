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
        self._gauss = GAUSS_S3
        self._type = 'S3'
        
    def updateFreedomSignature(self):
        '''
        Update node freedom signature for nodes in element.
        '''
        for node in self.nodes:
            if node.NFS[0] == 0:
                node.NFS[0] = 1
            if node.NFS[1] == 0:
                node.NFS[1] = 1
                
    def calculate_B_Matrix(self):
        '''
        Calculate the B-matrix (3, 6) given specific node coordinates.
        '''
        A = (self.nodes[1].coord[0] *self.nodes[2].coord[1] - \
			 self.nodes[2].coord[0] *self.nodes[1].coord[1] + \
			 self.nodes[2].coord[0] *self.nodes[0].coord[1] - \
			 self.nodes[0].coord[0] *self.nodes[2].coord[1] + \
			 self.nodes[0].coord[0] *self.nodes[1].coord[1] - \
			 self.nodes[1].coord[0] *self.nodes[0].coord[1])*0.5
        
        tempVal = 0.5 / A
        
        B = np.array([[self.nodes[1].coord[1] -self.nodes[2].coord[1] ,0.0,
					   self.nodes[2].coord[1] -self.nodes[0].coord[1] ,0.0,
					   self.nodes[0].coord[1] -self.nodes[1].coord[1] ,0.0],
					  [0.0,self.nodes[2].coord[0] -self.nodes[1].coord[0] ,
					   0.0,self.nodes[0].coord[0] -self.nodes[2].coord[0] ,
					   0.0,self.nodes[1].coord[0] -self.nodes[0].coord[0] ],
					  [self.nodes[2].coord[0] -self.nodes[1].coord[0] ,
					   self.nodes[1].coord[1] -self.nodes[2].coord[1] ,
					   self.nodes[0].coord[0] -self.nodes[2].coord[0] ,
					   self.nodes[2].coord[1] -self.nodes[0].coord[1] ,
					   self.nodes[1].coord[0] -self.nodes[0].coord[0] ,
					   self.nodes[0].coord[1] -self.nodes[1].coord[1] ]])*tempVal

        return B
    
    def getNodesDisplacement(self):
        '''
        Calculate the displacement vector (6, ) of the integral point.
        '''
        # TEST
        U = np.array([1, 2, 3, 0, 0, 0])
        return U.T
      
    def calculate_Strain(self):
        B = self.calculate_B_Matrix()
        U = self.getNodesDisplacement()
        strain_tensor = np.dot(B, U)
        self._solutions['E'] = strain_tensor
        print(strain_tensor)