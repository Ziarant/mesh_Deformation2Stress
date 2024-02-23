from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor, QQuaternion, QMouseEvent, QWheelEvent, QKeyEvent
from PyQt5.QtCore import QPointF
from pyqtgraph.Qt.QtCore import Qt
import pyqtgraph.opengl as gl
import numpy as np


class C3DWidget(gl.GLViewWidget):
    def __init__(self, parent:QWidget):
        super().__init__(parent)
        self._parent = parent
        
        # 键鼠控制
        self.mousePos = QPointF()
        self.MousePressed_Left:bool = False
        self.MousePressed_Right:bool = False
        self.MousePressed_Mid:bool = False
        self.ctrlPressed:bool = False
        self.altPressed:bool = False
        self.shiftPressed:bool = False
        
        # 视角初始化：
        self.initView()
        
        # 坐标轴
        self.initAxis()
        
    def initView(self):
        # 视角模式及初始化
        self.opts['rotationMethod'] = "quaternion"
        self.opts['distance'] = 500.0
        self.opts['fov'] = 60
        self.opts['rotation'] = QQuaternion(-0.35355427861213684, 0.14644664525985718, 0.3535540699958801, 0.8535544872283936)
        # rect = self.geometry()
        # w, h = rect.width(), rect.height()
        # self.opts['viewport'] = (0, 0, w, h)
        self.reset()
        self.dis = None
        self.ele = None
        self.azi = None
        self.installEventFilter(self)
        
    def reset(self):
        center = self.opts['center']
        fov = self.opts['fov']
        super().reset()
        self.opts['distance'] = 500.0
        self.opts['center'] = center
        self.opts['fov'] = fov
        self._bgColor = QColor(215, 225, 225)
        self.setBackgroundColor(self._bgColor)
        
    def initAxis(self):
        # 初始控件：视角中心
        self.viewCenter = gl.GLScatterPlotItem(pos = np.array([0, 0, 0]), size = 10, color = np.array([1.0, 0, 0, 1.0]))
        self.viewCenter.setGLOptions('additive')
        self.addItem(self.viewCenter)
        
        # 坐标轴-全局坐标系
        self.sysAxis = gl.GLAxisItem()
        self.sysAxis.setSize(x = 50, y = 50, z = 50)
        self.addItem(self.sysAxis)
        
        # 坐标轴设置, X-红色，Y-绿色， Z-蓝色
        a, b = gl.GLAxisItem(), gl.GLAxisItem()
        a.setSize(x=100, y=100, z=100)
        b.setSize(x=-100, y=-100, z=-100)
        a_line = np.array(([-100,0,0], [100,0,0]))
        b_line = np.array(([0,-100,0], [0,100,0]))
        c_line = np.array(([0,0,-100], [0,0,100]))
        width = 2
        self.aline = gl.GLLinePlotItem(pos = a_line, color = (.8, .8, .1, .6), width = width)       # x轴
        self.bline = gl.GLLinePlotItem(pos = b_line, color = (0, 1, 0, .6), width = width)          # y轴
        self.cline = gl.GLLinePlotItem(pos = c_line, color = (0, 0, 1, .6), width = width)          # z轴
        
        # 坐标轴箭头
        x_line = np.array(([90,-10,0], [100,0,0], [90,10,0]))
        y_line = np.array(([0,90,-10], [0,100,0], [0,90,10]))
        z_line = np.array(([10,0,90], [0,0,100], [-10,0,90]))
        self.xline = gl.GLLinePlotItem(pos = x_line, color = (.8, .8, .1, .6), width = width)
        self.yline = gl.GLLinePlotItem(pos = y_line, color = (0, 1, 0, .6), width = width)
        self.zline = gl.GLLinePlotItem(pos = z_line, color = (0, 0, 1, .6), width = width)
        
        # 坐标轴标注
        self.oText = gl.GLTextItem()
        self.xText = gl.GLTextItem()
        self.yText = gl.GLTextItem()
        self.zText = gl.GLTextItem()
        self.oText.setData(pos = (0, 0, 0), text = 'O', color = (255, 0, 0))
        self.xText.setData(pos = (120, 0, 0), text = 'X', color = (200, 200, 35))
        self.yText.setData(pos = (0, 120, 0), text = 'Y', color = (0, 255, 0))
        self.zText.setData(pos = (0, 0, 120), text = 'Z', color = (23, 35, 255))
        
        # 开启抗锯齿
        self.xline.antialias = True
        self.yline.antialias = True
        self.zline.antialias = True
        self.aline.antialias = True
        self.bline.antialias = True
        self.cline.antialias = True
        
        # 添加坐标轴控件
        self.xline.setParentItem(self.sysAxis)
        self.yline.setParentItem(self.sysAxis)
        self.zline.setParentItem(self.sysAxis)
        self.aline.setParentItem(self.sysAxis)
        self.bline.setParentItem(self.sysAxis)
        self.cline.setParentItem(self.sysAxis)
        self.oText.setParentItem(self.sysAxis)
        self.xText.setParentItem(self.sysAxis)
        self.yText.setParentItem(self.sysAxis)
        self.zText.setParentItem(self.sysAxis)
        
    def mousePressEvent(self, event:QMouseEvent):
        # 鼠标事件
        lpos = event.position() if hasattr(event, 'position') else event.localPos()
        self.mousePos = lpos
        
        if event.buttons () == Qt.LeftButton:
            self.MousePressed_Left = True
        
        if event.buttons () == Qt.RightButton:
            self.MousePressed_Right = True
        
        if event.buttons () == Qt.MidButton:
            self.MousePressed_Mid = True
            
        if self.MousePressed_Mid and self.ctrlPressed:
            self.reset()
        
    def wheelEvent(self, event:QWheelEvent):
        delta = - event.angleDelta().y() / 12
        # self.cMainWindow()
        if self.ctrlPressed == True:
            self.opts['distance'] += delta
            self.dis = self.opts['distance']
            self.dis = int(self.dis)
            self.update()
            
    def mouseMoveEvent(self, event:QMouseEvent):
        lpos = event.position() if hasattr(event, 'position') else event.localPos()
        diff = lpos - self.mousePos
        if self.MousePressed_Left and self.ctrlPressed:
            # ctrl+左键：旋转视角
            self.orbit(-diff.x(), diff.y())
        elif self.MousePressed_Right and self.ctrlPressed:
            # ctrl+右键：拖动视角
            self.pan(diff.x(), diff.y(), 0, relative='view')
        self.mousePos = lpos
            
    def mouseReleaseEvent(self, event:QMouseEvent):
        self.MousePressed_Left = False
        self.MousePressed_Right = False
        self.MousePressed_Mid = False
        
    def keyPressEvent(self, event:QKeyEvent):
        if event.key() == Qt.Key_Control:
            self.ctrlPressed = True    
        if event.key() == Qt.Key_Shift:
            self.shiftPressed = True
        if event.key() == Qt.Key_Alt:
            self.altPressed = True
            
    def keyReleaseEvent(self, event:QKeyEvent):
        if event.key() == Qt.Key_Control:
            self.ctrlPressed = False
        if event.key() == Qt.Key_Shift:
            self.shiftPressed = False
        if event.key() == Qt.Key_Alt:
            self.altPressed = False
            
    def orbit(self, azim, elev):
        # 重写orbit函数，取消视角转动限制
        """Orbits the camera around the center position. *azim* and *elev* are given in degrees."""
        if self.opts['rotationMethod'] == 'quaternion':
            q = QQuaternion.fromEulerAngles(
                    elev, -azim, 0
                    ) # rx-ry-rz
            q *= self.opts['rotation']
            self.opts['rotation'] = q
        else:
            self.opts['azimuth'] += azim
            self.opts['elevation'] += + elev
        self.update()