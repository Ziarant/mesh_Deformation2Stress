class BaseSection(object):
    _nextId = 1
    def __init__(self):
        self._id = BaseSection._nextId
        BaseSection._nextId += 1
        self._name = None
        
    def setName(self, name):
        self._name = name
        
    @property
    def name(self):
        return self._name