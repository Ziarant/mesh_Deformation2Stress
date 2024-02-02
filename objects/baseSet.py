class BaseSet(object):
    _nextId = 1
    def __init__(self):
        self._id = BaseSet._nextId
        BaseSet._nextId += 1
        
    @property
    def id(self):
        return self._id