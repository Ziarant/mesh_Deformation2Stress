import sys
from pyqtgraph.opengl.GLViewWidget import GLViewWidget

sys.path.append("..")
from conversion.loadInp import LoadInp
from _parser.parser import Parser
from _parser.handler import Handler

def importInp(inpFileName:str, viewport:GLViewWidget = None) -> Handler:
    '''
    import inp file and return a FEM-Handler object
    '''
    inpLoader = LoadInp(inpFileName)
    parser = Parser(inpLoader)
    modelHandle = Handler(parser, viewport)
    
    modelName = inpFileName.split("\\")[-1]
    modelHandle.setName(modelName[:-4])
    return modelHandle
    