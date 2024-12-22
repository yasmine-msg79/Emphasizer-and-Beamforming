import numpy as np
import cv2
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox
from regionSelector import ResizableRectangle  # Assuming you have a separate file for ResizableRectangle

class FourierComponents:
    def __init__(self, Gimage1, current_images, Fourier_comboBox_1, Fourier_comboBox_2, Fourier_comboBox_3, Fourier_comboBox_4, weight_1, weight_2, weight_3, weight_4, fourierimage1, fourierimage2, fourierimage3, fourierimage4):
        self.Gimage1 = Gimage1
        self.Fourier_comboBox_1 = Fourier_comboBox_1
        self.Fourier_comboBox_2 = Fourier_comboBox_2
        self.Fourier_comboBox_3 = Fourier_comboBox_3
        self.Fourier_comboBox_4 = Fourier_comboBox_4
        self.checkboxes = [Fourier_comboBox_1, Fourier_comboBox_2, Fourier_comboBox_3, Fourier_comboBox_4]
        self.weight_1 = weight_1
        self.weight_2 = weight_2
        self.weight_3 = weight_3
        self.weight_4 = weight_4

        self.fourierimage1 = fourierimage1
        self.fourierimage2 = fourierimage2
        self.fourierimage3 = fourierimage3
        self.fourierimage4 = fourierimage4
        self.ft_components = [{}, {}, {}, {}]
        self.current_images = current_images
        # self.current_images = [None, None, None, None]
        self.rects = {}

        self.Fourier_comboBox_1.currentIndexChanged.connect(lambda: self.update_ft_component(0))
        self.Fourier_comboBox_2.currentIndexChanged.connect(lambda: self.update_ft_component(1))
        self.Fourier_comboBox_3.currentIndexChanged.connect(lambda: self.update_ft_component(2))
        self.Fourier_comboBox_4.currentIndexChanged.connect(lambda: self.update_ft_component(3))

    def change_choices_combobox(self, magnitude_phase, real_imaginary):
        for combobox in self.checkboxes:
            if magnitude_phase.isChecked():
                combobox.setItemText(0, "FT Magnitude")
                combobox.setItemText(1, "FT Phase")
            else:
                combobox.setItemText(0, "FT Real")
                combobox.setItemText(1, "FT Imaginary")

    def compute_ft_components(self, frame):
        ft = np.fft.fft2(self.current_images[frame])
        ft_shifted = np.fft.fftshift(ft)

        self.ft_components[frame] = {
            "FT Magnitude": np.log1p(np.abs(ft_shifted)),
            "FT Phase": np.angle(ft_shifted),
            "FT Real": np.real(ft_shifted),
            "FT Imaginary": np.imag(ft_shifted),
        }

    def update_ft_component(self, index):
        if index == 0:
            selected_component = self.Fourier_comboBox_1.currentText()
            currentFourierImage = self.fourierimage1
            self.update_weight(0, self.weight_1.value())
        elif index == 1:
            selected_component = self.Fourier_comboBox_2.currentText()
            currentFourierImage = self.fourierimage2
            self.update_weight(1, self.weight_2.value())
        elif index == 2:
            selected_component = self.Fourier_comboBox_3.currentText()
            currentFourierImage = self.fourierimage3
            self.update_weight(2, self.weight_3.value())
        elif index == 3:
            selected_component = self.Fourier_comboBox_4.currentText()
            currentFourierImage = self.fourierimage4
            self.update_weight(3, self.weight_4.value())

        if selected_component in self.ft_components[index]:
            component_image = self.ft_components[index][selected_component]
            component_image = cv2.normalize(component_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            q_image = QImage(component_image.data, 256, 256, 256, QImage.Format_Grayscale8)  # Assuming size 256x256
            pixmap = QPixmap.fromImage(q_image)
            currentFourierImage.clear()
            pixmap = pixmap.scaled(self.Gimage1.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            currentFourierImage.addPixmap(pixmap)
            currentFourierImage.setSceneRect(QRectF(pixmap.rect()))
            self.rects[index] = ResizableRectangle(x=10, y=10, width=245, height=130)
            currentFourierImage.addItem(self.rects[index])

    def update_weight(self, index, value):
        pass  # Implement the logic for updating the weight
