import sys
from .baseHandle import BaseHandle

sys.path.append("..")
from objects.baseElement import BaseElement

class ElementHandle(BaseHandle):
    def __init__(self, element:BaseElement):
        super().__init__()
        self._object = element
        
        self.initObject()