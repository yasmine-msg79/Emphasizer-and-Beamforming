from PyQt5 import QtWidgets, QtGui, QtCore, uic  # Added uic import
import sys
from PyQt5.QtGui import *
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QGraphicsSceneMouseEvent
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QSlider, QSpinBox
)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('task4.ui', self)
        
        self.min_width = 0
        self.min_height = 0

        # Connect add array button click signal to the slot function
        self.add_array_button.clicked.connect(self.add_new_array)

        # Connect spinBox signal to the slot function
        self.spinBox_No_transmitters.valueChanged.connect(self.update_frequency_phase_table)
        
        # Initialize array counter
        self.array_counter = 2
        self.array_data = {}  # Dictionary to store table data for each array

        # Initialize array1 in combobox and default state in table
        self.comboBox_arrays.addItem("Array1")
        self.array_data["Array1"] = [(1, 0)]   # Initially, Array1 has 1 row in the table
        self.update_frequency_phase_table(1)

        # Connect the comboBox selection change to switch tables
        self.comboBox_arrays.currentIndexChanged.connect(self.switch_array)

        # Connect buttons to their methods
        self.switch_button.clicked.connect(self.hide_image_frame_and_label)
        self.return_button.clicked.connect(self.show_image_frame_and_label)
        self.frame_5.hide()
        self.image1.mouseDoubleClickEvent = lambda event: self.open_file(1, event)
        self.image2.mouseDoubleClickEvent = lambda event: self.open_file(2, event)
        self.image3.mouseDoubleClickEvent = lambda event: self.open_file(3, event)
        self.image4.mouseDoubleClickEvent = lambda event: self.open_file(4, event)
        self.scene = QtWidgets.QGraphicsScene()
        self.image1.setScene(self.scene)
        self.scene2 = QtWidgets.QGraphicsScene()
        self.image2.setScene(self.scene2)
        self.scene3 = QtWidgets.QGraphicsScene()
        self.image3.setScene(self.scene3)
        self.scene4 = QtWidgets.QGraphicsScene()
        self.image4.setScene(self.scene4)
        self.scene_output1 = QtWidgets.QGraphicsScene()
        self.output_mixer1.setScene(self.scene_output1)
        self.scene_output2 = QtWidgets.QGraphicsScene()
        self.output_mixer2.setScene(self.scene_output2)
        self.fourierimage1 = QtWidgets.QGraphicsScene()
        self.Gimage1.setScene(self.fourierimage1)
        self.fourierimage2 = QtWidgets.QGraphicsScene()
        self.Gimage2.setScene(self.fourierimage2)
        self.fourierimage3 = QtWidgets.QGraphicsScene()
        self.Gimage3.setScene(self.fourierimage3)
        self.fourierimage4 = QtWidgets.QGraphicsScene()
        self.Gimage4.setScene(self.fourierimage4)
        self.current_images = [None,None,None,None]
        self.output1_image = None
        self.ft_components = [{},{},{},{}]
        self.Fourier_comboBox_1.currentIndexChanged.connect(lambda: self.update_ft_component(0))
        self.Fourier_comboBox_2.currentIndexChanged.connect(lambda: self.update_ft_component(1))
        self.Fourier_comboBox_3.currentIndexChanged.connect(lambda: self.update_ft_component(2))
        self.Fourier_comboBox_4.currentIndexChanged.connect(lambda: self.update_ft_component(3))
        self.checkboxes = [self.Fourier_comboBox_1,self.Fourier_comboBox_2,self.Fourier_comboBox_3,self.Fourier_comboBox_4]
        
        self.weights = [0,0,0,0]
        self.weight_1.valueChanged.connect(lambda value: self.update_weight(0, value))
        self.weight_2.valueChanged.connect(lambda value: self.update_weight(1, value))
        self.weight_3.valueChanged.connect(lambda value: self.update_weight(2, value))
        self.weight_4.valueChanged.connect(lambda value: self.update_weight(3, value))
        self.weights_sliders = [self.weight_1, self.weight_2,self.weight_3,self.weight_4]
        
        self.change_choices_combobox()
        self.magnitude_phase.toggled.connect(self.change_choices_combobox)
        self.real_imaginary.toggled.connect(self.change_choices_combobox)
        
        self.output1.toggled.connect(self.change_output_location)
        self.output2.toggled.connect(self.change_output_location)
        self.frequency_phase_table_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row in range(3):
            for col in range(2):
                self.add_custom_widget(row, col)

    def add_custom_widget(self, row, col):
        widget = QWidget()
        uic.loadUi("table_item.ui", widget)
        self.frequency_phase_table_2.setCellWidget(row, col, widget)
        


    def open_file(self, frame, mouseevent):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if file_name:
            pixmap = QtGui.QPixmap(file_name)
            image = pixmap.toImage()
            image = image.convertToFormat(QtGui.QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(image)
            if self.min_width == 0 and self.min_height == 0:
                self.min_width = image.width()
                self.min_height = image.height()
            else:
                width = image.width()
                height = image.height()
                print("original: ",width, height)
                self.min_width = min(width, self.min_width)
                self.min_height = min(height, self.min_height)
                print("Min: ",self.min_width, self.min_height)
                      
            ptr = image.bits()
            ptr.setsize(self.min_width * self.min_height)
            if frame == 1:
                self.scene.clear()
                pixmap = pixmap.scaled(self.image1.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene.addPixmap(pixmap)
                self.scene.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.image1.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
                self.current_images[frame - 1] = np.array(ptr).reshape(self.min_height, self.min_width)
                self.compute_ft_components(0)
                self.update_ft_component(0)
            
            elif frame == 2:
                self.scene2.clear()
                pixmap = pixmap.scaled(self.image2.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene2.addPixmap(pixmap)
                self.scene2.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.image2.fitInView(self.scene2.sceneRect(), QtCore.Qt.KeepAspectRatio)
                self.current_images[frame - 1] = np.array(ptr).reshape(self.min_height, self.min_width)
                self.compute_ft_components(1)
                self.update_ft_component(1)
            
            elif frame == 3:
                self.scene3.clear()
                pixmap = pixmap.scaled(self.image3.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene3.addPixmap(pixmap)
                self.scene3.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.image3.fitInView(self.scene3.sceneRect(), QtCore.Qt.KeepAspectRatio)
                self.current_images[frame - 1] = np.array(ptr).reshape(self.min_height, self.min_width)
                self.compute_ft_components(2)
                self.update_ft_component(2)    
            
            elif frame == 4:
                self.scene4.clear()
                pixmap = pixmap.scaled(self.image4.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene4.addPixmap(pixmap)
                self.scene4.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.image4.fitInView(self.scene4.sceneRect(), QtCore.Qt.KeepAspectRatio)
                self.current_images[frame - 1] = np.array(ptr).reshape(self.min_height, self.min_width)
                self.compute_ft_components(3)
                self.update_ft_component(3)
       
            
    def change_choices_combobox(self):
        for combobox in self.checkboxes:
            if self.magnitude_phase.isChecked():
                combobox.setItemText(0,"FT Magnitude")
                combobox.setItemText(1,"FT Phase")
            else:
                combobox.setItemText(0,"FT Real")
                combobox.setItemText(1,"FT Imaginary") 
        for i in range (4): # to change fourier images
            if self.current_images[i] is not None:
                self.update_ft_component(i) 
                mixed_image = self.compute_inverse_ft_components()
                if self.output1.isChecked():
                    self.display_output_image(self.output_mixer1, mixed_image)  
                else:
                    self.display_output_image(self.output_mixer2, mixed_image) 
                    
    
    def change_output_location(self):
        mixed_image = self.compute_inverse_ft_components()
        if self.output1.isChecked():
            self.display_output_image(self.output_mixer1, mixed_image)  
        elif self.output2.isChecked():
            self.display_output_image(self.output_mixer2, mixed_image)                                
    

    def compute_ft_components(self, frame):
        ft = np.fft.fft2(self.current_images[frame])
        ft_shifted = np.fft.fftshift(ft)

        self.ft_components[frame] = {
            "FT Magnitude": np.log1p(np.abs(ft_shifted)),  # avoid log(0)
            "FT Phase": np.angle(ft_shifted),
            "FT Real": np.real(ft_shifted),
            "FT Imaginary": np.imag(ft_shifted),
        }


    def compute_inverse_ft_components(self):
        reconstructed_image = None

        # Normalize slider weights
        magnitude_weights = [
            slider.value() / 100 if combobox.currentText() == "FT Magnitude" else 0
            for slider, combobox in zip(self.weights_sliders, self.checkboxes)
        ]
        phase_weights = [
            slider.value() / 100 if combobox.currentText() == "FT Phase" else 0
            for slider, combobox in zip(self.weights_sliders, self.checkboxes)
        ]
        real_weights = [
            slider.value() / 100 if combobox.currentText() == "FT Real" else 0
            for slider, combobox in zip(self.weights_sliders, self.checkboxes)
        ]
        imaginary_weights = [
            slider.value() / 100 if combobox.currentText() == "FT Imaginary" else 0
            for slider, combobox in zip(self.weights_sliders, self.checkboxes)
        ]

        if self.magnitude_phase.isChecked():
            ft_magnitude_sum = np.zeros((self.min_height, self.min_width))
            ft_phase_sum = np.zeros((self.min_height, self.min_width))

            for i in range(len(self.ft_components)):
                if self.current_images[i] is not None:
                    resized_magnitude = self.ft_components[i]["FT Magnitude"].reshape(self.min_height, self.min_width)
                    # resized_magnitude = self.ft_components[i]["FT Magnitude"][:self.min_height, :self.min_width]
                    # resized_magnitude = cv2.resize(self.ft_components[i]["FT Magnitude"], (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)
                    resized_phase = self.ft_components[i]["FT Phase"].reshape(self.min_height, self.min_width)

                    ft_magnitude_sum += resized_magnitude * magnitude_weights[i]
                    ft_phase_sum += resized_phase * phase_weights[i]

            # Reconstruct using magnitude and phase
            reconstructed_ft = np.multiply(np.expm1(ft_magnitude_sum), np.exp(1j * ft_phase_sum))
            mixed_image = np.fft.ifft2(np.fft.ifftshift(reconstructed_ft))
            reconstructed_image = np.abs(mixed_image)

        else:
            ft_real_sum = np.zeros((self.min_height, self.min_width))
            ft_imaginary_sum = np.zeros((self.min_height, self.min_width))

            for i in range(len(self.ft_components)):
                if self.current_images[i] is not None:
                    resized_real = self.ft_components[i]["FT Real"].reshape(self.min_height, self.min_width)
                    resized_imaginary = self.ft_components[i]["FT Imaginary"].reshape(self.min_height, self.min_width)

                    ft_real_sum += resized_real * real_weights[i]
                    ft_imaginary_sum += resized_imaginary * imaginary_weights[i]

            # Reconstruct using real and imaginary parts
            mixed_image = np.fft.ifft2(ft_real_sum + 1j * ft_imaginary_sum)
            reconstructed_image = np.abs(mixed_image)

        # Normalize to range [0, 255]
        if reconstructed_image is not None:
            reconstructed_image = (255 * (reconstructed_image / np.max(reconstructed_image))).astype(np.uint8)

        return reconstructed_image


    def update_ft_component(self, index):
        if index == 0:
            selected_component = self.Fourier_comboBox_1.currentText()
            currentFourierImage = self.fourierimage1
        elif index == 1:
            selected_component = self.Fourier_comboBox_2.currentText()
            currentFourierImage = self.fourierimage2
        elif index == 2:
            selected_component = self.Fourier_comboBox_3.currentText()
            currentFourierImage = self.fourierimage3
        elif index == 3:
            selected_component = self.Fourier_comboBox_4.currentText()
            currentFourierImage = self.fourierimage4          
        # selected_component = self.Fourier_comboBox_4.itemText(index)
        if selected_component in self.ft_components[index]:
            component_image = self.ft_components[index][selected_component]
            # print(component_image)
            component_image = cv2.normalize(component_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            height, width = component_image.shape
            q_image = QtGui.QImage(component_image.data, width, height, width, QtGui.QImage.Format_Grayscale8)
            pixmap = QtGui.QPixmap.fromImage(q_image)
            currentFourierImage.clear()
            pixmap = pixmap.scaled(self.Gimage1.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            currentFourierImage.addPixmap(pixmap)
            currentFourierImage.setSceneRect(QtCore.QRectF(pixmap.rect()))
            self.Gimage1.fitInView(currentFourierImage.sceneRect(), QtCore.Qt.KeepAspectRatio)
        else:
            QtWidgets.QMessageBox.warning(self, "Error", f"Component {selected_component} not found.")

    def hide_image_frame_and_label(self):
        """Hides imageFrame, frame_3, and label; shows everything else."""
        self.imageFrame.hide()
        self.frame_3.hide()
        for widget in self.findChildren(QtWidgets.QWidget):
            if widget.objectName() not in ['imageFrame', 'frame_3']:
                widget.show()

    def show_image_frame_and_label(self):
        """Shows imageFrame, frame_3, and label; hides everything else."""
        self.frame_5.hide()
        self.imageFrame.show()
        self.frame_3.show()
        
        
    def update_weight(self, frame, value):
        self.weights[frame] = value
        print("self.weights: ", self.weights)  
        mixed_image = self.compute_inverse_ft_components()
        print ("mixed Image: ", mixed_image)
        if self.output1.isChecked():
            self.display_output_image(self.output_mixer1, mixed_image)  
        else:
            self.display_output_image(self.output_mixer2, mixed_image)  
        
        
    def display_output_image(self, label, mixed_image):
        # Convert NumPy array to QImage
        height, width = mixed_image.shape
        bytes_per_line = width
        # Convert the data to bytes explicitly
        image_data = mixed_image.tobytes()

        # Create the QImage
        q_image = QImage(image_data, width, height, bytes_per_line, QImage.Format_Grayscale8)

        # Display the mixed image in the QGraphicsView
        scene = QGraphicsScene()
        pixmap_item = QGraphicsPixmapItem(QPixmap.fromImage(q_image))
        scene.addItem(pixmap_item)

        # Set the scene to the label
        label.setScene(scene)
        label.fitInView(pixmap_item, Qt.KeepAspectRatio)

    def update_frequency_phase_table(self, no_transmitters):
        table = self.frequency_phase_table
        
        # Set the number of rows in the table to match no_transmitters
        table.setRowCount(no_transmitters)

        # Get the selected array from combobox
        selected_array = self.comboBox_arrays.currentText()
        
        # If the array has existing data, populate the table with that data
        if selected_array in self.array_data:
            data = self.array_data[selected_array]
        else:
            data = []
        
        # Populate the table with frequency and phase values
        for row in range(no_transmitters):
            if row < len(data):
                # If the row data exists, populate it
                freq, phase = data[row]
                table.setItem(row, 0, QTableWidgetItem(str(freq)))
                table.setItem(row, 1, QTableWidgetItem(str(phase)))
            else:
                # Otherwise, use default values for new rows
                table.setItem(row, 0, QTableWidgetItem(f"Freq {row + 1}"))
                table.setItem(row, 1, QTableWidgetItem(f"Phase {row + 1}"))
    
    def add_new_array(self):
        
        # Add new option to the comboBox_arrays
        new_array_name = f"Array{self.array_counter}"
        self.comboBox_arrays.addItem(new_array_name)

        self.array_data[new_array_name] = [(1, 0)]
        
        # Reset the table with the default values for the new array (e.g., 1 transmitter initially)
        self.update_frequency_phase_table(1)

        # Reset the no.transmitters spinbox to 1
        self.spinBox_No_transmitters.setValue(1)
        
        # Increment the array counter
        self.array_counter += 1

    def switch_array(self):
        
        # Get the selected array name
        selected_array = self.comboBox_arrays.currentText()
        
        # Retrieve the number of transmitters (rows) saved for the selected array
        no_transmitters = self.array_data.get(selected_array, [])  # Default to 1 if not found
        
        # Update the frequency_phase_table with the saved number of rows
        self.update_frequency_phase_table(no_transmitters)
        
        # Update the spinBox_No_transmitters to match the saved number of rows
        self.spinBox_No_transmitters.setValue(no_transmitters)
        
    def update_array_data(self):
        selected_array = self.comboBox_arrays.currentText()
        no_transmitters = self.spinBox_No_transmitters.value()
        
        # Save the current number of rows (transmitters) for the selected array
        self.array_data[selected_array] = no_transmitters


              
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
