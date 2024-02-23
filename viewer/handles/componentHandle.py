import sys
from .baseHandle import BaseHandle

sys.path.append("..")
from objects.baseSection import BaseSection

class ComponentHandle(BaseHandle):
    def __init__(self, component:BaseSection):
        super().__init__()
        self._object = component
        
        self.initTreeItem()