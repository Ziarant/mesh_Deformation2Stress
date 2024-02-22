import os, sys, typing
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import pyqtgraph.opengl as gl

class CMainWindow(QMainWindow):
    def __init__(self):
        # 数据初始化
        
        self.path = os.path.dirname(__file__)
        
        super(CMainWindow, self).__init__()
        self.ui = loadUi(self.path + '\\mainWidget.ui', self)
        self.showMaximized()