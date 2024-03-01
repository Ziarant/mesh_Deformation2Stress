import os, sys
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.uic import loadUi

sys.path.append('..')
from functions import *
from viewer.widgets.c3DWidget import C3DWidget

class CMainWindow(QMainWindow):
    def __init__(self):
        # 数据初始化
        
        self.path = os.path.dirname(__file__)
        self.parentPath = os.path.dirname(self.path)
        
        super(CMainWindow, self).__init__()
        self.ui = loadUi(self.path + '\\uis\\mainWidget.ui', self)
        # self._initUI()
        self.showMaximized()
        
        # 绑定事件
        self.actionInp.triggered.connect(self.actionInp_clicked)
    
    def _initUI(self):
        _3DWidget = C3DWidget(self)
        self._3DLayout.addWidget(_3DWidget, 0, 0)
        
    def actionInp_clicked(self):
        inpName = QFileDialog.getOpenFileName(self, 
                                              caption = '选择inp',
                                              directory= self.parentPath,
                                              filter = 'inp(*.inp)')
        inpName = inpName[0]
        if inpName == '':
            return
        modelHandle = importInp(inpName, viewport = self.openGLWidget)
        modelHandle.setTreeWidget(self.modelTreeWidget)
        modelHandle.updateItems()