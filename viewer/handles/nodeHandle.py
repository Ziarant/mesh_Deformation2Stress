import sys
from .baseHandle import BaseHandle

sys.path.append("..")

class NodeHandle(BaseHandle):
    def __init__(self, node):
        super().__init__()
        self._object = node
        
        self.initObject()