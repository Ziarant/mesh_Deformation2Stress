class Part(object):
    _nextId = 1
    def __init__(self, name):
        self._id = Part._nextId
        Part._nextId += 1
        
        self._name = name
        
    @property
    def name(self):
        return self._name
    
    @property
    def id(self):
        return self._id