

TYPE = ['SCALAR', 'VECTOR', 'TENSOR_2D_PLANER', 'TENSOR_3D_PLANER']
POSITION = ['NODAL', 'INTEGRATION_POINT', 'CENTROID']

class BaseField(object):
    _nextId = 1
    def __init__(self):
        self._id = BaseField._nextId
        BaseField._nextId += 1
        
        self._name:str = 'Field-' + str(self.id)
        self._type:str = 'SCALAR'
        self._position:str = 'NODAL'
        self._labels:tuple = None
        self._data:tuple = None
        
    def setName(self, name:str):
        self._name = name
        
    def setType(self, type:str):
        if type in TYPE:
            self._type = type
        else:
            raise ValueError('Invalid type')
        
    def setPosition(self, position:str):
        if position in POSITION:
            self._position = position
        else:
            raise ValueError('Invalid position')
        
    def setData(self, data:tuple):
        self._data = data
        
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def type(self):
        return self._type
    
    @property
    def position(self):
        return self._position
    
    @property
    def labels(self) -> tuple:
        return self._labels
    
    @property
    def data(self) -> tuple:
        return self._data