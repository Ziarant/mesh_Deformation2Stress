import sys, typing
import numpy as np
from abc import ABC, abstractmethod

from .matrix.bMatrix import BMatrix
from .baseSet import BaseSet
from .baseSection import BaseSection

ELEMENTTYPELIST = ['S3', 'S4', 'S4R']

# Guss Qadrature : list[N, N]
GAUSS_S3 = [[0.666666667, 0.166666667, 0.166666667],
			[0.166666667, 0.666666667, 0.166666667],
			[0.166666667, 0.166666667, 0.666666667]]

GAUSS_S4 = [[0.585410196624968, 0.138196601125011, 0.138196601125011, 0.138196601125011],
			[0.138196601125011, 0.585410196624968, 0.138196601125011, 0.138196601125011],
			[0.138196601125011, 0.138196601125011, 0.585410196624968, 0.138196601125011],
			[0.138196601125011, 0.138196601125011, 0.138196601125011, 0.585410196624968]]

class BaseElement(ABC):
	'''
	Abstract Base Class for elements.
	'''

	_nextId = 1
 
	@abstractmethod
	def __init__(self):
		self._id = BaseElement._nextId
		BaseElement._nextId += 1
  
		self._label:str = ''
		self._component:BaseSet = None
		self._section:BaseSection = None
		self._nodes:list = []
  
		self._type:str = ''
		self._order:int = 1
		self._gauss:list = None
		self._B_Matrix = BMatrix(self)
		self._solutions = {}
  
		self.updateFreedomSignature()
  
	def setType(self, elemType:str):
		self._type = elemType
  
	def setComponent(self, comp:BaseSet):
		self._component = comp
  
	def setSection(self, sect:BaseSection):
		self._section = sect
  
	def setOrder(self, order:int):
		self._order = order
  
	def setGauss(self, gauss:list):
		self._gauss = gauss
  
	def check_nodes_has_U_Data(self) -> bool:
		'''
		Check whether all nodes have 'U' data.
		'''
		for node in self.nodes:
			if 'U' not in node.solutions.keys():
				return False
		return True

	def has_E_Data(self) -> bool:
		'''
		Check whether has 'E_Tensor' data.
		'''
		if 'E_Tensor' in self.solutions.keys():
			return True
		return False 
  
	def setSolution(self, key:str, value):
		valueTypeName = type(value).__name__
		if valueTypeName in ['str', 'float', 'int', 'list', 'ndarray', 'tuple']:
			self._solutions[key] = value
			return
        
		if valueTypeName == 'dict':
			if key not in self._solutions.keys():
				self._solutions[key] = {}
			for valuekey in value.keys():
				self._solutions[key][valuekey] = value[valuekey]
			return

	def getSolution(self, key:str):
		if key in self._solutions:
			return self._solutions[key]

	def outputSolution(self, key:str, key2:str = None):
		solution = self.getSolution(key)
		if type(solution).__name__ == 'dict':
			if key2:
				solution = solution[key2]
			else:
				key2 = ''
		output = 'Element label:{} \t {} \t {} \t value: \t{}'.format(self.label, key, key2, solution)		
		print(output)
  
	def updateFreedomSignature(self):
		pass

	def updateNodes(self):
		for node in self.nodes:
			node.appendElement(self)

	def calculate_B_Matrix(self):
		'''
        Calculate the B-Matrix (6, 3) given specific node coordinates.
        B-Matrix:Describe the relationship between displacement and strain
        '''
		self._B_Matrix.calculate()

	def calculate_Strain_Nodal(self):
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

	def calculate_Stress(self):
		E_Tensor = self.getSolution('E_Tensor')
		material = self.material
		elasticTensor = material.elasticTensor
		S_Tensor = np.dot(E_Tensor, elasticTensor)
		S_11, S_22, S_33, S_12, S_13, S_23 = S_Tensor[0], S_Tensor[1], S_Tensor[2], S_Tensor[3], S_Tensor[4], S_Tensor[5]
		self.setSolution('S_Tensor', S_Tensor)
		self.setSolution('S', {'S_11' : S_11,
                               'S_22' : S_22,
                               'S_33' : S_33,
                               'S_12' : S_12,
                               'S_13' : S_13,
                               'S_23' : S_23})
		for node in self.nodes:
			node.setSolution('S_Tensor', {str(self.label) : S_Tensor})

	@property
	def id(self):
		return self._id

	@property
	def label(self):
		return self._label

	@property
	def component(self):
		return self._component

	@property
	def section(self):
		return self._component.section

	@property
	def nodes(self):
		return self._nodes

	@property
	def solutions(self):
		return self._solutions

	@property
	def material(self):
		return self._component.material

	@property
	def B_Matrix(self):
		return self._B_Matrix.matrix

	@property
	def elemType(self):
		return self._type