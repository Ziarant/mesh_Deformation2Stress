import sys
from conversion.loadInp import LoadInp
from _parser.parser import Parser
from solver import UField, EField, SField

_sourceFile = sys.argv[1]
_targetFile = sys.argv[2]

if __name__ == "__main__":
    sourceLoader = LoadInp(_sourceFile)
    targetLoader = LoadInp(_targetFile)
    
    sourceParser = Parser(sourceLoader)
    targetParser = Parser(targetLoader, isSource = False)
    
    uField = UField(sourceParser, targetParser)
    eField = EField(sourceParser)
    sField = SField(sourceParser)
    
    # eField.print()
    
# Test:
# python main.py test\source.inp test\target.inp