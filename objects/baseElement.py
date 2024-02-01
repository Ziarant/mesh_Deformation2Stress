import numpy as np

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
	def __init__(self, label:int, sect, nodes:list):
		self._id = BaseElement._nextId
		BaseElement._nextId += 1

		self._label = label
		self._section = sect
		self._nodes = nodes
		self._solutions = {}
  
		self.updateFreedomSignature()
  
	def updateFreedomSignature(self):
		pass
  
	def calculate_Strain(self):
		pass

	@property
	def label(self):
		return self._label

	@property
	def section(self):
		return self._section

	@property
	def nodes(self):
		return self._nodes