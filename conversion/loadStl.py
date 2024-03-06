import sys, os
import open3d as o3d
import numpy as np
from stl import mesh

sys.path.append('..')
from .loader import BaseLoader

class LoadStl(BaseLoader):
    def __init__(self, path):
        super().__init__(path)
        self._path = path
        self._partName = 'Part-1'
        self._points:dict = {}
        self.parseStl()
        
    def parseStl(self):
        '''
        解析stl文件,注册为Node和S3单元：
        '''
        stlMesh = self.path
        if isinstance(stlMesh, str):
            if not os.path.exists(stlMesh):
                return
            self._partName = os.path.basename(stlMesh)[:-4]
            self._parts = [self._partName]
        stlFile = open(stlMesh, 'rb')
        stlInfo, stlData = mesh.Mesh.load(stlFile)
        stlModel = mesh.Mesh(data=stlData)
        self._vectors = stlModel.vectors

        self._countNode = 0
        self._countElement = 0
        self._nodes = []
        self._elements = {'S3' : {self._partName : []}}
        for vector in self._vectors:
            self.register(vector)
            
        self._sections = {self._partName : ['SHELLSECTION', self._partName, None, None]}
            
    def register(self, vector):
        '''
        注册节点和S3单元：
        '''
        N1 = self.registerNode(vector[0])
        N2 = self.registerNode(vector[1])
        N3 = self.registerNode(vector[2])
        self._countElement += 1
        self._elements['S3'][self._partName].append([self._countElement, N1[0], N2[0], N3[0], self._partName])
            
    def registerNode(self, node):
        x, y, z = node[0], node[1], node[2]
        if str(x) in self._points.keys():
            if str(y) in self._points[str(x)].keys():
                if str(z) in self._points[str(x)][str(y)].keys():
                    return self._points[str(x)][str(y)][str(z)]
                else:
                    self._countNode += 1
                    self._points[str(x)][str(y)][str(z)] = [self._countNode, x, y, z, self._partName]
                    self._nodes.append([self._countNode, x, y, z, self._partName])
                    return [self._countNode, x, y, z, self._partName]
            else:
                self._countNode += 1
                self._points[str(x)][str(y)] = {}
                self._nodes.append([self._countNode, x, y, z, self._partName])
                return [self._countNode, x, y, z, self._partName]
        else:
            self._countNode += 1
            self._points[str(x)] = {}
            self._nodes.append([self._countNode, x, y, z, self._partName])
            return [self._countNode, x, y, z, self._partName]
            
    @property
    def path(self):
        return self._path