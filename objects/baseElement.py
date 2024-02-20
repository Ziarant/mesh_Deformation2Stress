import sys, typing
import numpy as np
from abc import ABC, abstractmethod

from .matrix.sMatrix import SMatrix
from .matrix.jMatrix import JMatrix
from .matrix.bMatrix import BMatrix
from .baseSet import BaseSet
from .baseSection import BaseSection

ELEMENTTYPELIST = ['S3', 'S4', 'S4R']

# Guss Qadrature : list[N, N]
GAUSS_S3 = [[1.0/3, 1.0/3, 1.0/3]]

GAUSS_S4 = [[-np.sqrt(3)/3, -np.sqrt(3)/3],
            [np.sqrt(3)/3, -np.sqrt(3)/3],
            [np.sqrt(3)/3, np.sqrt(3)/3],
            [-np.sqrt(3)/3, np.sqrt(3)/3]]

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
  
		self._integralPoint:list = []
  
		self._is3D:bool = True

		self._type:str = ''
		self._order:int = 1
		self._gauss:list = None
		self._gaussWidget:float = 1.0
		self._gaussPoints:list = []
		self._S_Matrix = SMatrix(self)
		self._J_Matrix = JMatrix(self)
		self._B_Matrix = BMatrix(self)
		self._solutions = {}
  
		self.updateFreedomSignature()
  
	def setType(self, elemType:str):
		self._type = elemType
  
	def set3D(self, is3D:bool):
		self._is3D = is3D
  
	def setComponent(self, comp:BaseSet):
		self._component = comp
  
	def setSection(self, sect:BaseSection):
		self._section = sect
  
	def setNodes(self, nodes:list):
		self._nodes = nodes
		self.updateNodes()
		self.calIntegralPoint()
  
	def setOrder(self, order:int):
		self._order = order
  
	def setGauss(self, gauss:list):
		self._gauss = gauss
  
	def setGaussWidget(self, gaussWidget:float):
		self._gaussWidget = gaussWidget
  
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

	def setGaussPoints(self, gaussPoints:list):
		'''
		设置高斯积分点（局部坐标系），高斯积分点数目与单元类型和阶数有关。
		'''
		self._gaussPoints = gaussPoints

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
		self.calIntegralPoint()

	def calIntegralPoint(self):
		'''
		Calculate the integral point of element.
		'''
		coordMatrix = []
		for node in self.nodes:
			coordMatrix.append(node.coord)
   
		if self.gauss is None:
			return

		# gaussM = np.array(self.gauss)
		# coordM = np.array(coordMatrix)

		# pointM = np.dot(gaussM, coordM)
		# _integralPoint = np.sum(pointM, axis=0) * self.gaussWidget
		_integralPoint = [0, 0, 0]
		self._integralPoint = [_integralPoint[0], _integralPoint[1], _integralPoint[2]]

	def calculate_B_Matrix(self):
		'''
        Calculate the B-Matrix (6, 3) given specific node coordinates.
        B-Matrix:Describe the relationship between displacement and strain
        '''
		self._S_Matrix.calculate()
		self._J_Matrix.calculate()
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
		N = len(self.nodes)
		strain_tensor = np.zeros((N, 6))
		for i in range(3):
			node = self.nodes[i]
			E_Tensor_Nodal = node.getSolution('E_Tensor_Nodal')
			strain_tensor[i] = E_Tensor_Nodal[str(self.label)]
         
        # Warning: Element Strain is not simple average of Nodal Strain.
        # The element strain should be calculated by the displacement of the integral point.
        # The displacement of the integral point should be calculated by each node and shape function
		# E_T = np.dot(self.gauss, strain_tensor)
		E_Tensor = np.sum(strain_tensor, axis = 0)
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
	def is3D(self):
		return self._is3D

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
	def integralPoint(self):
		return self._integralPoint

	@property
	def solutions(self):
		return self._solutions

	@property
	def gauss(self) -> list:
		return self._gauss

	@property
	def gaussWidget(self) -> float:
		return self._gaussWidget

	@property
	def gaussPoints(self) -> list:
		return self._gaussPoints

	@property
	def material(self):
		return self._component.material

	@property
	def S_Matrix(self):
		return self._S_Matrix.matrix

	@property
	def NDiff(self):
		return self._S_Matrix.NDiff

	@property
	def J_Matrix(self):
		return self._J_Matrix.matrix

	@property
	def B_Matrix(self):
		return self._B_Matrix.matrix

	@property
	def elemType(self):
		return self._type

	@property
	def Jacobian(self):
		return self._J_Matrix.jacobian