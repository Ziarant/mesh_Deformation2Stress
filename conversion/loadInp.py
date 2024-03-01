import sys, re

sys.path.append('..')
from .loader import BaseLoader
    
def check_line_start(pattern:str, line:str, eliminate:str = None) -> bool:
    '''
    Check whether it is the starting line of nodes/elements/materials…
    eliminate: str. If the string is included, `False` is returned.
    '''
    # pattern = r'\*Element'
    if eliminate is not None:
        if re.search(eliminate, line, re.IGNORECASE):
            return False
    if re.search(pattern, line, re.IGNORECASE):
        return True
    else:
        return False
    
def getElementType(line:str):
    '''
    Get element type from the line.
    ---
    Example:
    line: *ELEMENT, TYPE=C3D8R, ELSET=Source
    '''
    line = line.strip()
    element_info = line.split(',')
    elemType = element_info[1].strip()[5:]
    if len(element_info) > 2:
        elemSet = element_info[2].strip()[6:]
    else:
        elemSet = None
    return elemType, elemSet

class LoadInp(BaseLoader):
    def __init__(self, path):
        super().__init__(path)
        self._path = path
        self._context = self.load()
        self.parseInp()
        
    def parseInp(self):
        node_start_line = 0
        element_start_line = 0
        material_start_line = 0
        currentPartName = 'Part-1'
        for idx, line in enumerate(self._context):
            if check_line_start(r'\*Part', line):
                part_start_line = idx
                currentPartName = self.parseParts(part_start_line)
            
            if check_line_start(r'\*Node', line, r'\*Node Output'):
                node_start_line = idx + 1
                self.parseNodes(node_start_line, partName=currentPartName)
                
            if check_line_start(r'\*Element', line):
                element_start_line = idx + 1
                elemType, elemSet = getElementType(line)
                self.parseElements(element_start_line, elemType, elemSet, currentPartName)
                
            if check_line_start(r'\*Material', line):
                material_start_line = idx
                self.parseMaterials(material_start_line)
                
            if check_line_start(r'\*SHELL SECTION,', line):
                shell_section_start_line = idx
                self.parseShellSection(shell_section_start_line)
            
        if node_start_line == 0:
            raise ValueError('No node line found in %s'%self.path)
        if element_start_line == 0: 
            raise ValueError('No element line found in %s'%self.path)
        if material_start_line == 0:
            print('Warning: No material line found in %s'%self.path)
            
    def parseParts(self, part_start_line:int):
        line = self._context[part_start_line]
        part_info = line.split('=')
        if len(part_info) == 1:
            partName = 'Part-1'
        else:
            partName = part_info[1].strip()
        self._parts.append(partName)
        return partName
    
    def parseNodes(self, node_start_line:int, partName:str = 'Part-1'):
        for line in self._context[node_start_line:]:
            line = line.strip()
            
            if line.startswith('*'):
                break
            
            node_info = line.split(',')
            label = node_info[0].strip()
            x = float(node_info[1].strip())
            y = float(node_info[2].strip())
            # Warning: It's not certain that it contains z
            z = float(node_info[3].strip())
            self._nodes.append([label, x, y, z, partName])
            
    def parseElements(self, elem_start_line:int, elemType:str, elemSet:str, partName = 'Part-1'):
        if elemSet is None:
            elemSet = 'Auto'
        if elemType not in self._elements.keys():
            self._elements[elemType] = {}
        if elemSet not in self._elements[elemType].keys():
            self._elements[elemType][elemSet] = []
            
        for line in self._context[elem_start_line:]:
            line = line.strip()

            if line.startswith('*'):
                break

            elem_info = line.split(', ')
            label = elem_info[0].strip()
            numNodes = len(elem_info) - 1
            
            data = [int(label)]
            for i in range(numNodes):
                nodeLabel = int(elem_info[i + 1].strip())
                data.append(nodeLabel)
            data.append(partName)
            self._elements[elemType][elemSet].append(data)
            
    def parseMaterials(self, material_start_line:int):
        '''
        '''
        mat_start_line = self._context[material_start_line]
        matStartLine = mat_start_line.split('=')
        matName = matStartLine[1].strip()
        
        mat_type_line = self._context[material_start_line + 1]
        # 当前只考虑弹性，忽略空材料设置及其他
        # TODO：更多材料选择
        if not re.search(r'\*Elastic', mat_type_line, re.IGNORECASE):
            return
        matTypeLine = mat_type_line.split('=')
        try:
            matType = matTypeLine[1].strip()
        except:
            matType = 'ISOTROPIC'
        
        mat_data_line = self._context[material_start_line + 2]
        matdata = []
        for data in mat_data_line.split(','):
            matdata.append(float(data.strip()))
        self._materials[matName] = [matType, matdata]
        
    def parseShellSection(self, shell_section_start_line:int):
        section_start_line = self._context[shell_section_start_line]
        sectionStartLine = section_start_line.split(',')
        elsetNameLine = sectionStartLine[1].strip()
        elsetName = elsetNameLine.split('=')[1].strip()
        
        matNameLine = sectionStartLine[2].strip()
        matName = matNameLine.split('=')[1].strip()
        
        section_data_line = self._context[shell_section_start_line + 1]
        sectionData = []
        for data in section_data_line.split(','):
            data = data.strip()
            if len(data) == 0:
                continue
            sectionData.append(float(data))
        self._sections[elsetName] = ['SHELLSECTION', elsetName, matName, sectionData]
            
    @property
    def path(self):
        return self._path
    
# loader.nodes: list[N] = [label, x, y, z]
# loader.element: dict[TYPE][ELSET] = [label, n1, n2, …]
# loader.properties:dict[NAME] = [TYPE, ELSET, MATERIAL, DATA]
# loader.materials:dict[NAME] = [TYPE, DATA]