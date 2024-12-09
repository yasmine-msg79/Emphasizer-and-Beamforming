from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from PyQt5.QtGui import *
# from gui import Ui_MainWindow
import numpy as np
import cv2
from PyQt5 import QtWidgets, uic
import sys
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('task4.ui', self)
        self.image1.mouseDoubleClickEvent = lambda event: self.open_file(1, event)
        self.image2.mouseDoubleClickEvent = lambda event: self.open_file(2, event)
        self.image3.mouseDoubleClickEvent = lambda event: self.open_file(3, event)
        self.image4.mouseDoubleClickEvent = lambda event: self.open_file(4, event)
        self.scene = QtWidgets.QGraphicsScene()
        self.image1.setScene(self.scene)
        self.scene2 = QtWidgets.QGraphicsScene()
        self.image2.setScene(self.scene2)
        # self.scene3 = QtWidgets.QGraphicsScene()
        # self.ui.image3.setScene(self.scene3)
        self.scene4 = QtWidgets.QGraphicsScene()
        self.image4.setScene(self.scene4)
        self.fourierimage1 = QtWidgets.QGraphicsScene()
        self.Gimage1.setScene(self.fourierimage1)
        self.current_image = None
        self.ft_components = {}
        self.Fourier_comboBox_1.currentIndexChanged.connect(self.update_ft_component)
        self.Fourier_comboBox_2.currentIndexChanged.connect(self.update_ft_component)
        self.Fourier_comboBox_3.currentIndexChanged.connect(self.update_ft_component)
        self.Fourier_comboBox_4.currentIndexChanged.connect(self.update_ft_component)

    def open_file(self, frame, mouseevent):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if file_name:
            pixmap = QtGui.QPixmap(file_name)
            image = pixmap.toImage()
            image = image.convertToFormat(QtGui.QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(image)
            if frame == 1:
                self.scene.clear()
                pixmap = pixmap.scaled(self.image1.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene.addPixmap(pixmap)
                self.scene.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.image1.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
                width = image.width()
                height = image.height()
                ptr = image.bits()
                ptr.setsize(height * width)
                self.current_image = np.array(ptr).reshape(height, width)
                self.compute_ft_components()
                self.update_ft_component(0)                
            elif frame == 2:
                self.scene2.clear()
                pixmap = pixmap.scaled(self.image2.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene2.addPixmap(pixmap)
                self.scene2.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.ui.image2.fitInView(self.scene2.sceneRect(), QtCore.Qt.KeepAspectRatio)
            # elif frame == 3:
            #     self.scene3.clear()
            #     pixmap = pixmap.scaled(self.ui.image3.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            #     self.scene3.addPixmap(pixmap)
            #     self.scene3.setSceneRect(QtCore.QRectF(pixmap.rect()))
            #     self.ui.image3.fitInView(self.scene3.sceneRect(), QtCore.Qt.KeepAspectRatio)
            elif frame == 4:
                self.scene4.clear()
                pixmap = pixmap.scaled(self.image4.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene4.addPixmap(pixmap)
                self.scene4.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.ui.image4.fitInView(self.scene4.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def compute_ft_components(self):
        ft = np.fft.fft2(self.current_image)
        ft_shifted = np.fft.fftshift(ft)

        self.ft_components = {
            "FT Magnitude": np.log(1 + np.abs(ft_shifted)),
            "FT Phase": np.angle(ft_shifted),
            "FT Real": ft_shifted.real,
            "FT Imaginary": ft_shifted.imag
        }

    def update_ft_component(self, index):

        selected_component = self.ui.Fourier_comboBox_4.itemText(index)
        if selected_component in self.ft_components:
            component_image = self.ft_components[selected_component]
            component_image = cv2.normalize(component_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            height, width = component_image.shape
            q_image = QtGui.QImage(component_image.data, width, height, width, QtGui.QImage.Format_Grayscale8)
            pixmap = QtGui.QPixmap.fromImage(q_image)
            self.fourierimage1.clear()
            pixmap = pixmap.scaled(self.ui.Gimage1.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.fourierimage1.addPixmap(pixmap)
            self.fourierimage1.setSceneRect(QtCore.QRectF(pixmap.rect()))
            self.Gimage1.fitInView(self.fourierimage1.sceneRect(), QtCore.Qt.KeepAspectRatio)
        else:
            QtWidgets.QMessageBox.warning(self, "Error", f"Component {selected_component} not found.")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
