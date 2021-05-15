from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.picshow = QtWidgets.QGraphicsView(self.centralWidget)
        self.picshow.setObjectName("picshow")
        self.gridLayout.addWidget(self.picshow, 0, 1, 3, 1)
        self.zoomout = QtWidgets.QPushButton(self.centralWidget)
        self.zoomout.setObjectName("zoomout")
        self.gridLayout.addWidget(self.zoomout, 0, 0, 1, 1)
        self.zoomin = QtWidgets.QPushButton(self.centralWidget)
        self.zoomin.setObjectName("zoomin")
        self.gridLayout.addWidget(self.zoomin, 1, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.zoomout.setText(_translate("MainWindow", "放大"))
        self.zoomin.setText(_translate("MainWindow", "缩小"))

    然后生成事件对话框代码，在
    picturezoom类中，添加初始化变量，使在运行界面时显示图像“lena.jpg”具体代码如下。注意在本例程中，利用的时python - opencv3第三方开发库的cv2.imread()
    函数导入图像，需要进行颜色通道的转换。QT5中关于QtWidgets.QGraphicsView框架的相关内容较为复杂，本文中不详细介绍，给出参考链接。

    img = cv2.imread("lena.jpg")  # 读取图像
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换图像通道
    x = img.shape[1]  # 获取图像大小
    y = img.shape[0]
    self.zoomscale = 1  # 图片放缩尺度
    frame = QImage(img, x, y, QImage.Format_RGB888)
    pix = QPixmap.fromImage(frame)
    self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
    # self.item.setScale(self.zoomscale)
    self.scene = QGraphicsScene()  # 创建场景
    self.scene.addItem(self.item)
    self.picshow.setScene(self.scene)  # 将场景添加至视图


然后添加单击按钮的的事件函数，利用QGraphicsPixmapItem中
setScale()
方法实现图源大小的缩放。代码如下：

@pyqtSlot()
def on_zoomin_clicked(self):
    """
    点击缩小图像
    """
    # TODO: not implemented yet
    self.zoomscale = self.zoomscale - 0.05
    if self.zoomscale <= 0:
        self.zoomscale = 0.2
    self.item.setScale(self.zoomscale)  # 缩小图像


@pyqtSlot()
def on_zoomout_clicked(self):
    """
    点击方法图像
    """
    # TODO: not implemented yet
    self.zoomscale = self.zoomscale + 0.05
    if self.zoomscale >= 1.2:
        self.zoomscale = 1.2
    self.item.setScale(self.zoomscale)  # 放大图像


实现效果如下：
完整代码如下：

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QImage, QPixmap
import cv2
from Ui_picshow import Ui_MainWindow


class picturezoom(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(picturezoom, self).__init__(parent)
        self.setupUi(self)
        img = cv2.imread("lena.jpg")  # 读取图像
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换图像通道
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(img, x, y, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        # self.item.setScale(self.zoomscale)
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.picshow.setScene(self.scene)  # 将场景添加至视图

    @pyqtSlot()
    def on_zoomin_clicked(self):
        """
        点击缩小图像
        """
        # TODO: not implemented yet
        self.zoomscale = self.zoomscale - 0.05
        if self.zoomscale <= 0:
            self.zoomscale = 0.2
        self.item.setScale(self.zoomscale)  # 缩小图像

    @pyqtSlot()
    def on_zoomout_clicked(self):
        """
        点击方法图像
        """
        # TODO: not implemented yet
        self.zoomscale = self.zoomscale + 0.05
        if self.zoomscale >= 1.2:
            self.zoomscale = 1.2
        self.item.setScale(self.zoomscale)  # 放大图像


def main():
    import sys
    app = QApplication(sys.argv)
    piczoom = picturezoom()
    piczoom.show()
    app.exec_()


if __name__ == '__main__':
    main()
def show_3d_model(self,filename=""):#显示3D数据
        "获取选择零件名称  获取路径"
        #获取零件名称
        pass
        self.partname=""
        #获取相应零件的路径
        self.partpath=os.getcwd()
        self.partpath=self.partpath+"/3Ddata"+"/"+self.partname+".step"
        self.canva._display.EraseAll()# Delete part
        #self.canva._display.display_triedron()
        #self.canva._display.set_bg_gradient_color(background_gradient_color1, background_gradient_color2)
        try:
            shape=read_step_file(self.partpath)
            #shape = BRepPrimAPI_MakeBox(10, 10, 10).Shape()
            self.canva._display.DisplayShape(shape)
            self.canva._display.FitAll()
        except:
            pass

        return filename