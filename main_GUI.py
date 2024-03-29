# coding=utf-8
import sys, os, ctypes
# 强制使用单独的AppUserModelID-->新资源支配权限
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('myappid') 

from PyQt5.QtWidgets import *
from pyqtgraph.Qt import QtGui, QtCore

def app_exit():
        # 程序退出时的行为:清空变量
        app.exec_()
        key_list = []
        for key in globals().keys(): 
            if not key.startswith("__"):
                key_list.append(key)
        for key in key_list:
            globals().pop(key)

if __name__ == '__main__':
    from viewer.cMainWindow import CMainWindow
    # 在加载资源前调用QApplication
    app = QApplication(sys.argv)
    window = CMainWindow()
    window.show()
    
    sys.exit(app_exit())