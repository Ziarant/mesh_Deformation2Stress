import sys

sys.path.append("..")
from conversion.loadInp import LoadInp
from _parser.parser import Parser
from _parser.handler import Handler

def importInp(inpFileName:str):
    '''
    import inp file and return a FEM-Handler object
    '''
    inpLoader = LoadInp(inpFileName)
    parser = Parser(inpLoader)
    modelHandle = Handler(parser)
    
    modelName = inpFileName.split("\\")[-1]
    modelHandle.setName(modelName[:-4])
    return modelHandle
    