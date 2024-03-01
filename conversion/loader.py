import numpy as np

class BaseLoader(object):
    def __init__(self, path:str):
        self._path:str = path
        self._parts:list = []
        self._nodes:list = []
        self._elements:dict = {}
        self._sections:dict = {}
        self._properties:dict = {}
        self._materials:dict = {}       

    def load(self) -> str:
        with open(self._path, 'r') as f:
            return f.readlines()
        
    @property
    def nodes(self) -> list:
        return self._nodes
    
    @property
    def elements(self) -> dict:
        return self._elements
    
    @property
    def sections(self) -> dict:
        return self._sections
    
    @property
    def parts(self) -> list:
        if len(self._parts) == 0:
            self._parts = list(self.elements.keys())
            self._parts = ['Part-1']
        return self._parts
    
    @property
    def properties(self) -> dict:
        return self._properties
    
    @property
    def materials(self) -> dict:
        return self._materials
        
# loader.parts: list[P] = partName
# loader.nodes: list[N] = [label, x, y, z]
# loader.element: dict[TYPE][ELSET] = [label, n1, n2, …]
# loader.properties:dict[NAME] = [ELSET, MATERIAL, DATA]
# loader.materials:dict[NAME] = [TYPE, DATA]