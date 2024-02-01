import sys
from conversion.loadInp import LoadInp
from _parser.parser import Parser
from solver import *

_sourceFile = sys.argv[1]
_targetFile = sys.argv[2]

if __name__ == "__main__":
    sourceLoader = LoadInp(_sourceFile)
    targetLoader = LoadInp(_targetFile)
    
    sourceParser = Parser(sourceLoader)
    targetParser = Parser(targetLoader)
    
    UField(sourceParser, targetParser)
    EField(sourceParser, targetParser)