import sys
from .baseHandle import BaseHandle

sys.path.append("..")
from objects.baseMaterial import BaseMaterial

class MaterialHandle(BaseHandle):
    def __init__(self, material:BaseMaterial):
        super().__init__()
        self._object = material
        
        self.initTreeItem()