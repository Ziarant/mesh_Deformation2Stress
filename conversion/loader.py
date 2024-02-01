import numpy as np

class BaseLoader(object):
    def __init__(self, path:str):
        self._path:str = path
        self._nodes:list = []
        self._elements:dict = {}
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
    def properties(self) -> dict:
        return self._properties
    
    @property
    def materials(self) -> dict:
        return self._materials
        
        
# 输出形式：
# Node: list[N] = [label, x, y, z]
# Element: dict[TYPE][ELSET] = [label, n1, n2, …]
# Property:dict[NAME] = [ELSET, MATERIAL, DATA]
# Material:dict[NAME] = [TYPE, DATA]