import sys, typing
import numpy as np

from .matrix.bMatrix import BMatrix
from .baseSet import BaseSet
from .baseSection import BaseSection

ELEMENTTYPELIST = ['S3', 'S4', 'S4R']

GAUSS_S3 = [[0.666666667, 0.166666667, 0.166666667],
			[0.166666667, 0.666666667, 0.166666667],
			[0.166666667, 0.166666667, 0.666666667]]

GAUSS_S4 = [[0.585410196624968, 0.138196601125011, 0.138196601125011, 0.138196601125011],
			[0.138196601125011, 0.585410196624968, 0.138196601125011, 0.138196601125011],
			[0.138196601125011, 0.138196601125011, 0.585410196624968, 0.138196601125011],
			[0.138196601125011, 0.138196601125011, 0.138196601125011, 0.585410196624968]]

class BaseElement(object):
	'''
	Base class for elements.
	'''

	_nextId = 1
	def __init__(self, label:int, elemSet: BaseSet, nodes:list):
		self._id = BaseElement._nextId
		BaseElement._nextId += 1

		self._label = label
		self._elemSet = elemSet
		self._nodes = nodes
  
		self._type:str = ''
		self._order:int = 1
		self._gauss:list = None
		self._B_Matrix = BMatrix(self)
		self._solutions = {}
  
		self.updateFreedomSignature()
  
	def setType(self, elemType:str):
		self._type = elemType
  
	def setSect(self, sect):
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

	def calculate_B_Matrix(self):
		'''
        Calculate the B-Matrix (6, 3) given specific node coordinates.
        B-Matrix:Describe the relationship between displacement and strain
        '''
		self._B_Matrix.calculate()

	def calculate_Strain_Nodal(self):
		pass
  
	def calculate_Strain(self):
		pass

	def calculate_Stress(self):
		pass

	@property
	def id(self):
		return self._id

	@property
	def label(self):
		return self._label

	@property
	def section(self):
		return self._section

	@property
	def nodes(self):
		return self._nodes

	@property
	def solutions(self):
		return self._solutions

	@property
	def B_Matrix(self):
		return self._B_Matrix.matrix

	@property
	def elemType(self):
		return self._type