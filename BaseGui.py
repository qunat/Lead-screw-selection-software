# -*- coding: utf-8 -*-
#!/usr/bin/env python

import logging
import os
import sys
#import threading,time
import time
#from PyQt5 import QtSvg

from OCC.Core.BRepTools import breptools_Write

from OCC.Display.OCCViewer import OffscreenRenderer
from OCC.Display.backend import load_backend, get_qt_modules
from PyQt5.QtWidgets import QHBoxLayout, QDockWidget, \
    QListWidget, QFileDialog
#from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtWidgets
from graphics import GraphicsView, GraphicsPixmapItem
import Create_boll_Screw
import Vision




#------------------------------------------------------------开始初始化环境
log = logging.getLogger(__name__)
def check_callable(_callable):
    if not callable(_callable):
        raise AssertionError("The function supplied is not callable")
backend_str=None
size=[850, 873]
display_triedron=True
background_gradient_color1=[206, 215, 222]
background_gradient_color2=[128, 128, 128]
if os.getenv("PYTHONOCC_OFFSCREEN_RENDERER") == "1":
    # create the offscreen renderer
    offscreen_renderer = OffscreenRenderer()


    def do_nothing(*kargs, **kwargs):
        """ takes as many parameters as you want,
        ans does nothing
        """
        pass


    def call_function(s, func):
        """ A function that calls another function.
        Helpfull to bypass add_function_to_menu. s should be a string
        """
        check_callable(func)
        log.info("Execute %s :: %s menu fonction" % (s, func.__name__))
        func()
        log.info("done")

    # returns empty classes and functions
used_backend = load_backend(backend_str)
log.info("GUI backend set to: %s", used_backend)
#------------------------------------------------------------初始化结束
from OCC.Display.qtDisplay import qtViewer3d
import MainGui
from PyQt5.QtGui import QPixmap
QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()
from OCC.Extend.DataExchange import read_step_file,write_step_file
from OCC.Core.TopoDS import TopoDS_Shape,TopoDS_Builder,TopoDS_Compound,topods_CompSolid



class Mywindown(QtWidgets.QMainWindow,MainGui.Ui_MainWindow):
    pass
    def __init__(self, parent=None):
        super(Mywindown,self).__init__(parent)
        self.setupUi(self)
        #3D显示设置
        self.canva = qtViewer3d(self)#链接3D模块
        self.setWindowTitle("TBI-SFU系列【丝杆选型软件】")
        #self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setFixedSize(self.width(), self.height());
        self.canva.setGeometry(QtCore.QRect(370, 173, 470, 340))
        self.centerOnScreen()
        #------------------------------------------------------------------视图设置
        self.quit.triggered.connect(self.Quit)
        self.actionView_Right.triggered.connect(self.View_Right)
        self.actionView_Left.triggered.connect(self.View_Left)
        self.actionView_Top.triggered.connect(self.View_Top)
        self.actionView_Bottom.triggered.connect(self.View_Bottom)
        self.actionView_Front.triggered.connect(self.View_Front)
        self.actionView_Iso.triggered.connect(self.View_Iso)
        #------------------------------------------------------------尺寸数据显示设置
        pix = QPixmap('Pic\\pic1.jpg')
        self.graphicsView = GraphicsView(pix, self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(370, 530, 470, 280))
        self.graphicsView.setObjectName("graphicsView")
        self.item = GraphicsPixmapItem(pix)  # 创建像素图元
        self.scene = QtWidgets.QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)


        #------------------------------------------------------------滚动条
        self.widget.setMinimumSize(160, 700)#设置滚动范围
        self.scroll = QtWidgets.QScrollArea()#创建滚动类
        self.scroll.setWidget(self.widget)#设置滚动区域为self.widget

        self.vbox = QtWidgets.QVBoxLayout()#创建布局
        self.vbox.addWidget(self.scroll)#增加布局内容
        self.tab.setLayout(self.vbox)#

        self.widget_2.setMinimumSize(160, 700)  # 设置滚动范围
        self.scroll2 = QtWidgets.QScrollArea()  # 创建滚动类
        self.scroll2.setWidget(self.widget_2)  # 设置滚动区域为self.widget

        self.vbox2 = QtWidgets.QVBoxLayout()  # 创建布局
        self.vbox2.addWidget(self.scroll2)  # 增加布局内容
        self.tab_2.setLayout(self.vbox2)  #
        #--------------------------------------------------------------状态栏
        self.statusBar().showMessage('状态：软件运行正常')
        #self.setGeometry(300, 300, 250, 150)
        #---------------------------------------------------------------菜单栏


        #--------------------------------------------------------------控件更新信号
        self.comboBox.currentTextChanged.connect(self.updata_show)
        self.comboBox_6.currentTextChanged.connect(self.updata_show)
        self.comboBox_20.currentTextChanged.connect(self.updata_show)
        #self.comboBox.currentTextChanged.connect(self.show_3d_model)
        #self.comboBox_6.currentTextChanged.connect(self.show_3d_model)
        #self.comboBox_20.currentTextChanged.connect(self.show_3d_model)
        self.pushButton.clicked.connect(self.Show_3d_model)
        self.pushButton_2.clicked.connect(self.Copy_part_to_path)
        #-----------------------------------------------------------------------初始化变量
        self.shape = TopoDS_Shape
        self.filename=str()
        self.SFU = Create_boll_Screw.Create_boll_SCcrew()


    def View_Bottom(self):
        pass
        self.canva._display.View_Bottom()
    def View_Front(self):
        pass
        self.canva._display.View_Front()
    def View_Iso(self):
        pass
        self.canva._display.View_Iso()

    def View_Left(self):
        pass
        self.canva._display.View_Left()
    def View_Right(self):
        pass
        self.canva._display.View_Right()

    def View_Top(self):
        pass
        self.canva._display.View_Top()

    def centerOnScreen(self):
        '''Centers the window on the screen.'''
        resolution = QtWidgets.QApplication.desktop().screenGeometry()
        x = (resolution.width() - self.frameSize().width()) / 2
        y = (resolution.height() - self.frameSize().height()) / 2
        self.move(x, y)

    def Show_3d_model(self,filename="SFU2005-4"):#显示3D数据

        pass
        #更新显示
        try:
            self.canva._display.Context.Remove(self.show[0],True)
            self.aCompound.Free()
        except:
            pass
            #print("shibai")

        try:
            a1 = self.comboBox_6.currentText()  # 公称直径
            a2 = self.comboBox_20.currentText()  # 导程
            a3=self.comboBox_23.currentText()# 固定侧型号
            L=float(self.lineEdit.text())

            filename = "SFU"
            if len(a1) == 1:
                filename = filename + "00" + a1
            elif len(a1) == 2:
                filename = filename + "0" + a1
            elif len(a1) == 3:
                filename = filename + a1
            if len(a2) != 2:
                filename = filename + "0" + a2 + "-4"
            else:
                filename = filename + a2 + "-4"

            new_part=Create_boll_Screw.Create_boll_SCcrew()
            if 'BK' in a3:
                self.aCompound = new_part.Create_Bk(filename, L=L)
            elif "EK" in a3:
                self.aCompound = new_part.Create_Ek(filename, L=L)
            elif "FK" in a3:
                self.aCompound = new_part.Create_Fk(filename, L=L)


            self.show=self.canva._display.DisplayShape(self.aCompound,update=True)
            self.canva._display.View_Iso()
            self.canva._display.FitAll()
        except:
            pass
        self.filename=filename
        return filename

    def Copy_part_to_path(self):  #生成数据到指定路径
        try:
            try:
                a1 = self.comboBox_6.currentText()  # 公称直径
                a2 = self.comboBox_20.currentText()  # 导程
                a3 = self.comboBox_23.currentText()  # 固定侧型号
                L = float(self.lineEdit.text())

                filename = "SFU"
                if len(a1) == 1:
                    filename = filename + "00" + a1
                elif len(a1) == 2:
                    filename = filename + "0" + a1
                elif len(a1) == 3:
                    filename = filename + a1
                if len(a2) != 2:
                    filename = filename + "0" + a2 + "-4"
                else:
                    filename = filename + a2 + "-4"

                new_part = Create_boll_Screw.Create_boll_SCcrew()
                if 'BK' in a3 and float(a1)<=55:
                    self.aCompound = new_part.Create_Bk(filename, L=L)
                elif "EK" in a3 and float(a1)<=36:
                    self.aCompound = new_part.Create_Ek(filename, L=L)
                elif "FK" in a3 and float(a1)<=50:
                    self.aCompound = new_part.Create_Fk(filename, L=L)
                else:
                    self.statusBar().showMessage('错误：没有此类型丝杆')

            except:
                pass
            self.filename = filename
            path="D:\\"+self.filename
            fileName, ok = QFileDialog.getSaveFileName(self, "文件保存", path, "All Files (*);;Text Files (*.step)")
            fileName=fileName.split("/")
            fileName=fileName[0]+"\\"+fileName[1]+"\\"+fileName[2]
            write_step_file(self.aCompound, fileName)
            #breptools_Write(self.aCompound, 'box.brep')
        except:
            pass

    def updata_show(self):#更新显示界面ß
        pass
        try:
            a1=self.comboBox_6.currentText()#公称直径
            a2=self.comboBox_20.currentText()#导程
            filename="SFU"
            if len(a1)==1:
                filename=filename+"00"+a1
            elif len(a1)==2:
                filename=filename+"0"+a1
            elif len(a1)==3:
                filename=filename+a1
            if len(a2)!=2:
                filename=filename+"0"+a2+"_4"
            else:
                filename=filename+a2+"_4"
            print(filename)
            self.label_125.setText(filename)
            self.label_74.setText(str(self.SFU.SFU_serise_dict[filename]["Da"]))
            self.label_76.setText(str(self.SFU.SFU_serise_dict[filename]["N"]))  # 循环系列
            self.label_6.setText(str(self.SFU.SFU_serise_dict[filename]["D"]))  # D
            self.label_7.setText(str(self.SFU.SFU_serise_dict[filename]["A"]))  # A
            self.label_9.setText(str(self.SFU.SFU_serise_dict[filename]["B"]))  # B
            self.label_26.setText(str(self.SFU.SFU_serise_dict[filename]["L"]))  # L
            self.label_27.setText(str(self.SFU.SFU_serise_dict[filename]["L"]))  # W
            self.label_32.setText(str(self.SFU.SFU_serise_dict[filename]["X"]))  # X
            self.label_33.setText(str(self.SFU.SFU_serise_dict[filename]["H"]))  # H
            self.label_34.setText(str(self.SFU.SFU_serise_dict[filename]["Q"]))  # Q
            self.label_94.setText(str(self.SFU.SFU_serise_dict[filename]["Ca"]))  # Ca
            self.label_95.setText(str(self.SFU.SFU_serise_dict[filename]["Coa"]))  # Coa
            self.label_96.setText(str(self.SFU.SFU_serise_dict[filename]["kgf/um"]))  # kgf/um
            self.statusBar().showMessage('状态：软件运行正常')
        except:
            pass
            self.statusBar().showMessage('错误：没有此类型丝杆')
            self.label_74.setText("--")  # 滚珠直径
            self.label_76.setText("--")  # 循环系列
            self.label_125.setText("--")
            self.label_125.setText("--")
            self.label_74.setText("--")  # 滚珠直径
            self.label_76.setText("--")  # 循环系列
            self.label_6.setText("--")  # D
            self.label_7.setText("--")  # A
            self.label_9.setText("--")  # B
            self.label_26.setText("--")  # L
            self.label_27.setText("--")  # W
            self.label_32.setText("--")  # X
            self.label_33.setText("--")  # H
            self.label_34.setText("--")  # Q
            self.label_35.setText("--")  # Q
            self.label_94.setText("--")  # Ca
            self.label_95.setText("--")  # Coa
            self.label_96.setText("--")  # kgf/um

        print(filename)

    def Quit(self):#退出
        self.close()

    def Vision(self):#版本显示
        pass




class Vision(QtWidgets.QMainWindow,Vision.Ui_Form):
    def __init__(self,parent=None):
        super(Vision, self).__init__(parent)
        self.setupUi(self)
        self.label_6.setText("<A href='https://www.onlinedown.net/'>软件下载：https://www.onlinedown.net/</a>")
        self.label_6.setOpenExternalLinks(True)





# following couple of lines is a tweak to enable ipython --gui='qt'
if __name__ == '__main__':
    app = QtWidgets.QApplication.instance()  # checks if QApplication already exists
    if not app:  # create QApplication if it doesnt exist
        app = QtWidgets.QApplication(sys.argv)
    #启动界面
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap("Pic\\setup_pic.jpg"))#启动图片设置
    splash.show()
    splash.showMessage("软件启动中......")
    time.sleep(0.5)
    #--------------------
    win = Mywindown()
    win_vision=Vision()
    win.vision.triggered.connect(win_vision.show)
    win.show()
    win.centerOnScreen()
    win.canva.InitDriver()
    win.resize(size[0], size[1])
    win.canva.qApp = app

    display = win.canva._display
    display.display_triedron()
    if background_gradient_color1 and background_gradient_color2:
    # background gradient
        display.set_bg_gradient_color(background_gradient_color1, background_gradient_color2)
    win.raise_()  # make the application float to the top
    splash.finish(win)
    app.exec_()