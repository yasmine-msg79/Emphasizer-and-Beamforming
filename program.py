from PyQt5 import QtWidgets, QtGui, QtCore, uic   # Added uic import
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
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QSpinBox, QVBoxLayout, QDoubleSpinBox, QHeaderView
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QSlider, QSpinBox)
import scenarios
from visualizer import Visualizer
from PIL import Image


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('task4.ui', self)
        
        
        self.min_width = 0
        self.min_height = 0

        # Connect buttons to their methods
        self.switch_button.clicked.connect(self.hide_image_frame_and_label)
        self.return_button.clicked.connect(self.show_image_frame_and_label)
        self.frame_5.hide()
        self.image1.mouseDoubleClickEvent = lambda event: self.open_file(1, event)
        self.image2.mouseDoubleClickEvent = lambda event: self.open_file(2, event)
        self.image3.mouseDoubleClickEvent = lambda event: self.open_file(3, event)
        self.image4.mouseDoubleClickEvent = lambda event: self.open_file(4, event)
        self.scene1 = QtWidgets.QGraphicsScene()
        self.image1.setScene(self.scene1)
        self.scene2 = QtWidgets.QGraphicsScene()
        self.image2.setScene(self.scene2)
        self.scene3 = QtWidgets.QGraphicsScene()
        self.image3.setScene(self.scene3)
        self.scene4 = QtWidgets.QGraphicsScene()
        self.image4.setScene(self.scene4)
        self.scenes = [self.scene1, self.scene2, self.scene3, self.scene4]
        self.loaded_images = [self.image1,self.image2,self.image3,self.image4]
        self.loaded_files = [None, None, None, None]
        
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
        self.preserved_images= [None,None,None,None]
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

        self.mouse_pressed = False
        self.active_frame = None
      
        self.brightness = [0] * 4  # Assuming 4 frames
        self.contrast = [1.0] * 4

        for i in range(1, 5):  
            image = getattr(self, f"image{i}")
            image.setMouseTracking(True)
            image.mouseMoveEvent = lambda event, i=i: self.mouse_movement(event, i-1)
            image.mousePressEvent = lambda event, i=i: self.mouse_press(event, i-1)
            image.mouseReleaseEvent = self.mouse_release
        
        self.change_choices_combobox()
        self.magnitude_phase.toggled.connect(self.change_choices_combobox)
        self.real_imaginary.toggled.connect(self.change_choices_combobox)
        
        self.output1.toggled.connect(self.change_output_location)
        self.output2.toggled.connect(self.change_output_location)

        self.Fourier_comboBox_1.currentIndexChanged.connect(lambda:self.apply_region(self.region_selecter.value()))
        self.Fourier_comboBox_2.currentIndexChanged.connect(lambda:self.apply_region(self.region_selecter.value()))
        self.Fourier_comboBox_3.currentIndexChanged.connect(lambda:self.apply_region(self.region_selecter.value()))
        self.Fourier_comboBox_4.currentIndexChanged.connect(lambda:self.apply_region(self.region_selecter.value()))
        self.region_selecter.valueChanged.connect(self.apply_region)
        self.in_region_radioButton.toggled.connect(lambda:self.apply_region(self.region_selecter.value()))
        self.out_region_radioButton.toggled.connect(lambda:self.apply_region(self.region_selecter.value()))


        ################# PART B #########################
        #  Find and initialize UI elements
        self.linear_radio_button = self.findChild(QtWidgets.QRadioButton, "linear_radio_button_3")
        self.frequency_slider = self.findChild(QtWidgets.QSlider, "beam_frequency_slider")
        self.phase_slider = self.findChild(QtWidgets.QSlider, "beam_phase_slider")
        self.curvature_slider = self.findChild(QtWidgets.QSlider, "beam_curvature_slider")
        self.no_transmitters_spinbox = self.findChild(QtWidgets.QSpinBox, "spinBox_No_transmitters_3")
        self.frequency_lcd = self.findChild(QtWidgets.QLCDNumber, "frequency_lcd")
        self.phase_lcd = self.findChild(QtWidgets.QLCDNumber, "phase_lcd")
        self.curvature_lcd = self.findChild(QtWidgets.QLCDNumber, "curvature_lcd")
        self.beam_position_slider = self.findChild(QtWidgets.QSlider, "beam_position_slider")
        self.position_lcd = self.findChild(QtWidgets.QLCDNumber, "position_lcd")


        self.beam_map_view = self.findChild(QtWidgets.QWidget, "beam_map")
        self.beam_plot_view = self.findChild(QtWidgets.QWidget, "beam_plot")
        self.scenario_combobox = self.findChild(QtWidgets.QComboBox, "comboBox_Open_scenario")

        # Initialize parameters
        self.num_transmitters = 2
        self.frequencies = [1000000] * self.num_transmitters  # Default frequency for each transmitter
        self.phases = [0] * self.num_transmitters  # Default phase for each transmitter
        self.array_type = "curved"  # Default to curved
        self.curvature_angle = 0.0  # Default curvature angle
        self.element_spacing = 0.5  # Default element spacing
        self.array_position = [0, 0]  # Default position of the array

        # Set the initial state of radio button
        self.linear_radio_button.setChecked(False)
        self.update_radio_button_text(self.linear_radio_button.isChecked())
        self.linear_radio_button.toggled.connect(self.update_radio_button_text)

        # Connect UI elements to methods
        self.frequency_slider.setMinimum(1000000000)
        self.frequency_slider.setMaximum(2000000000)
        self.frequency_slider.setSingleStep(10000000)  # Step size
        self.frequency_slider.valueChanged.connect(self.update_frequency)
        self.phase_slider.setMinimum(-180)
        self.phase_slider.setMaximum(180)
        self.phase_slider.valueChanged.connect(self.update_phase)
        self.curvature_slider.setMinimum(1)
        self.curvature_slider.setMaximum(360)
        self.curvature_slider.valueChanged.connect(self.update_curvature_angle)
        self.no_transmitters_spinbox.setMinimum(2)
        self.no_transmitters_spinbox.setMaximum(100)
        self.no_transmitters_spinbox.valueChanged.connect(self.update_transmitter_count)
        self.beam_position_slider.setMinimum(-10)
        self.beam_position_slider.setMaximum(10)
        self.beam_position_slider.setSingleStep(1)
        self.beam_position_slider.valueChanged.connect(self.update_array_position)

        self.scenario_combobox.currentIndexChanged.connect(self.update_scenario_parameters)

        # Initialize the plots
        self.beam_forming()

        
    def open_file(self, frame, mouseevent):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_name:
            self.loaded_files[frame - 1] = file_name
            pixmap = QtGui.QPixmap(file_name)
            image = pixmap.toImage()
            image = image.convertToFormat(QtGui.QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(image)
            
            # Update min_width and min_height
            if self.min_width == 0 and self.min_height == 0:
                self.min_width = image.width()
                self.min_height = image.height()
            else:
                width = image.width()
                height = image.height()
                print("original: ", width, height)
                self.min_width = min(width, self.min_width)
                self.min_height = min(height, self.min_height)
                print("Min: ",self.min_width, self.min_height)
                     
            image_calculations = Image.open(file_name).convert('L')
            resize_image_calculations = image_calculations.resize((self.min_width ,self.min_height))
            self.current_images[frame - 1] = resize_image_calculations
            self.preserved_images[frame-1]=resize_image_calculations
            ptr = image.bits()
            ptr.setsize(self.min_width * self.min_height)
            if frame == 1:
                self.scene1.clear()
                pixmap = pixmap.scaled(self.min_width, self.min_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene1.addPixmap(pixmap)
                self.scene1.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.image1.fitInView(self.scene1.sceneRect(), QtCore.Qt.KeepAspectRatio)
                self.compute_ft_components(0)
                self.update_ft_component(0)

            elif frame == 2:
                self.scene2.clear()
                pixmap = pixmap.scaled(self.min_width, self.min_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene2.addPixmap(pixmap)
                self.scene2.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.image2.fitInView(self.scene2.sceneRect(), QtCore.Qt.KeepAspectRatio)
                self.compute_ft_components(1)
                self.update_ft_component(1)

            elif frame == 3:
                self.scene3.clear()
                pixmap = pixmap.scaled(self.min_width, self.min_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene3.addPixmap(pixmap)
                self.scene3.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.image3.fitInView(self.scene3.sceneRect(), QtCore.Qt.KeepAspectRatio)
                self.compute_ft_components(2)
                self.update_ft_component(2)

            elif frame == 4:
                self.scene4.clear()
                pixmap = pixmap.scaled(self.min_width, self.min_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene4.addPixmap(pixmap)
                self.scene4.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.image4.fitInView(self.scene4.sceneRect(), QtCore.Qt.KeepAspectRatio)
                self.compute_ft_components(3)
                self.update_ft_component(3)
            self.resize_images()      
            
            
    def resize_images(self):
        for i in range(4):
            if self.current_images[i] is not None: 
                # Open and resize the image
                image = Image.open(self.loaded_files[i]).convert('L')
                resized_image = image.resize((self.min_width, self.min_height))

                # Convert to NumPy array and then to QImage
                np_array = np.array(resized_image, dtype=np.uint8)
                byte_data = np_array.tobytes()
                qimage = QImage(byte_data, self.min_width, self.min_height, self.min_width, QImage.Format_Grayscale8)
                
                # Convert QImage to QPixmap and display it
                pixmap = QPixmap.fromImage(qimage)
                self.scenes[i].clear()
                self.scenes[i].addPixmap(pixmap)
                self.scenes[i].setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.loaded_images[i].fitInView(self.scenes[i].sceneRect(), QtCore.Qt.KeepAspectRatio)
                
                print(f"Image {i} resized to {self.min_width}x{self.min_height}")
                # to resize the ft image also     
                self.update_ft_component(i)

            

        # # Ensure the image is loaded for the given frame
        # if self.current_images[frame - 1] is not None:

        #     # Check if in-region or out-region radio button is selected
        #     if self.in_region_radioButton.isChecked() or self.out_region_radioButton.isChecked():
        #         # Add a resizable rectangle to the scene
        #         rect_item = self.addResizableRectangle(
        #             self.Gimage1.scene(),
        #             self.current_images[frame - 1],  # Pass the correct current image
        #             self.region_selecter.value(),
        #             self.region_selecter.value(),
        #             self.in_region_radioButton.isChecked()
        #         )

        # else:
        #     QtWidgets.QMessageBox.warning(self, "Error", "No image loaded for the selected frame.")

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
                    self.display_output_image(self.output_mixer1, self.scene_output1, mixed_image)  
                else:
                    self.display_output_image(self.output_mixer2, self.scene_output2, mixed_image) 
                    
    
    def change_output_location(self):
        mixed_image = self.compute_inverse_ft_components()
        if self.output1.isChecked():
            self.display_output_image(self.output_mixer1, self.scene_output1, mixed_image)  
        elif self.output2.isChecked():
            self.display_output_image(self.output_mixer2, self.scene_output2, mixed_image)                                
    

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
                    resized_magnitude = cv2.resize(self.ft_components[i]["FT Magnitude"], (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)
                    resized_phase = cv2.resize(self.ft_components[i]["FT Phase"], (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)
                    ft_magnitude_sum += resized_magnitude * magnitude_weights[i]
                    ft_phase_sum += resized_phase * phase_weights[i]

            # Reconstruct using magnitude and phase
            reconstructed_ft = np.multiply(np.expm1(ft_magnitude_sum), np.exp(1j * ft_phase_sum))
            reconstructed_image =  np.abs(np.fft.ifft2(np.fft.ifftshift(reconstructed_ft)))

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
            max_val = np.max(reconstructed_image)
            reconstructed_image = (255 * (reconstructed_image / max_val)).astype(np.uint8) if max_val > 0 else np.zeros_like(reconstructed_image, dtype=np.uint8)

        return reconstructed_image


    def update_ft_component(self, index):
        if index == 0:
            selected_component = self.Fourier_comboBox_1.currentText()
            currentFourierImage = self.fourierimage1
            self.update_weight(0, self.weight_1.value())
            print("frame1")
        elif index == 1:
            selected_component = self.Fourier_comboBox_2.currentText()
            currentFourierImage = self.fourierimage2
            self.update_weight(1, self.weight_2.value())
            print("frame2")
        elif index == 2:
            selected_component = self.Fourier_comboBox_3.currentText()
            currentFourierImage = self.fourierimage3
            self.update_weight(2, self.weight_3.value())
            print("frame3")
        elif index == 3:
            selected_component = self.Fourier_comboBox_4.currentText()
            currentFourierImage = self.fourierimage4
            self.update_weight(3, self.weight_4.value())          

        if selected_component in self.ft_components[index]:
            component_image = self.ft_components[index][selected_component]
            component_image = cv2.normalize(component_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            q_image = QtGui.QImage(component_image.data, self.min_width, self.min_height, self.min_width, QtGui.QImage.Format_Grayscale8)
            pixmap = QtGui.QPixmap.fromImage(q_image)
            currentFourierImage.clear()
            pixmap = pixmap.scaled(self.Gimage1.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            currentFourierImage.addPixmap(pixmap)
            currentFourierImage.setSceneRect(QtCore.QRectF(pixmap.rect()))
            self.Gimage1.fitInView(currentFourierImage.sceneRect(), QtCore.Qt.KeepAspectRatio)
           
        else:
            QtWidgets.QMessageBox.warning(self, "Error", f"Component {selected_component} not found.")

    def hide_image_frame_and_label(self):
        # Hides imageFrame, frame_3, and label; shows everything else
        self.imageFrame.hide()
        self.frame_3.hide()
        for widget in self.findChildren(QtWidgets.QWidget):
            if widget.objectName() not in ['imageFrame', 'frame_3']:
                widget.show()

    def show_image_frame_and_label(self):
        # Shows imageFrame, frame_3, and label; hides everything else
        self.frame_5.hide()
        self.imageFrame.show()
        self.frame_3.show()
        
    def update_weight(self, frame, value):
        self.weights[frame] = value
        mixed_image = self.compute_inverse_ft_components()
        if self.output1.isChecked():
            self.display_output_image(self.output_mixer1, self.scene_output1, mixed_image)  
        else:
            self.display_output_image(self.output_mixer2, self.scene_output1, mixed_image)  
        
        
    def display_output_image(self, label, scene, mixed_image):
        # Clear the previous output
        scene.clear()
        
        # convert NumPy array to QImage
        height, width = mixed_image.shape

        # convert the data to bytes
        image_data = mixed_image.tobytes()

        # create the QImage
        q_image = QtGui.QImage(image_data, width, height, width, QtGui.QImage.Format_Grayscale8)
        pixmap = QtGui.QPixmap.fromImage(q_image)
        
        pixmap = pixmap.scaled(label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        scene.addPixmap(pixmap)
        scene.setSceneRect(QtCore.QRectF(pixmap.rect()))
        label.fitInView(scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def mouse_press(self, event, frame_index):
        self.mouse_pressed = True
        self.active_frame = frame_index
        self.last_mouse_pos = event.pos()


    def mouse_movement(self, event, frame_index):
        if self.mouse_pressed and self.active_frame == frame_index:
            delta = event.pos() - self.last_mouse_pos

            # Adjust contrast and brightness dynamically
            self.brightness[frame_index] += delta.y()
            self.contrast[frame_index] += delta.x() * 0.01
            self.contrast[frame_index] = max(0.1, self.contrast[frame_index]) 
            self.adjust_brightness_contrast(frame_index)
            print(frame_index)
            self.compute_ft_components(frame_index)
            self.update_ft_component(frame_index)
            self.last_mouse_pos = event.pos()


    def mouse_release(self, event):
        self.mouse_pressed = False
        self.active_frame = None
        self.last_mouse_pos = None


    def adjust_brightness_contrast(self, frame):
            # print(self.current_images[frame])
            # previous_image=self.current_images[frame]
            original_image = np.array(self.preserved_images[frame])
          
            # Apply contrast and brightness adjustments
            adjusted = self.contrast[frame] * original_image + self.brightness[frame]
           
           
            adjusted = np.clip(adjusted, 0, 255).astype(np.uint8) 
            height, width = adjusted.shape
            image_data = adjusted.tobytes()
            q_image = QtGui.QImage(image_data,self.min_width, self.min_height, self.min_width, QtGui.QImage.Format_Grayscale8)
            pixmap = QtGui.QPixmap.fromImage(q_image)
            print(self.current_images[frame])
            print(q_image)
            print(pixmap)
            # print(image_data)

            scene = getattr(self, f"scene{frame + 1}")
            scene.clear()
            scene.addPixmap(pixmap)
           
            
            
            getattr(self, f"image{frame + 1}").fitInView(scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
            pil_image = Image.fromarray(adjusted, mode="L")
            self.current_images[frame]=pil_image
            print(self.current_images[frame])


    def apply_region(self, value):
        """
        Applies the region mask to the current Fourier component based on the rectangle.
        The region is adjusted using the region_selector slider.
        """
        for frame in range(1, 5):  # Loop through all frames (1-4)
            if self.current_images[frame - 1] is not None:  # Ensure image is loaded for the frame
                # Update Fourier component for the current frame
                self.update_ft_component(frame - 1)

                # Get the image data and scene for the frame
                img_data = self.current_images[frame - 1]
                scene = self.get_scene_for_frame(frame)  # Retrieve the scene for the current frame

                # Add a resizable rectangle to the scene
                if self.out_region_radioButton.isChecked() or self.in_region_radioButton.isChecked():
                    rect_item = self.addResizableRectangle(
                        scene,
                        self.convert_component_to_qimage(img_data),  # Convert the image component
                        value, 
                        value,
                        self.in_region_radioButton
                    )
                    self.masked_img_comp = self.extractRegion(rect_item, self.convert_component_to_qimage(img_data), img_data, self.in_region_radioButton)


    def extractRegion(self, rect_item, image_component, image_component_array, inner_region_selected):
        image_component = QGraphicsPixmapItem(QPixmap.fromImage(image_component))
        rect_scene_pos = rect_item.scenePos()
        rect_scene_rect = rect_item.rect()
        rect_image_pos = image_component.mapFromScene(rect_scene_pos)
        rect_image_rect = image_component.mapFromScene(rect_scene_rect).boundingRect()

        if inner_region_selected.isChecked():
            mask = np.zeros_like(image_component_array)
            mask[int(rect_image_pos.y()):int(rect_image_pos.y() + rect_image_rect.height()),
                int(rect_image_pos.x()):int(rect_image_pos.x() + rect_image_rect.width())] = 1
        else:
            mask = np.ones_like(image_component_array)
            mask[int(rect_image_pos.y()):int(rect_image_pos.y() + rect_image_rect.height()),
            int(rect_image_pos.x()):int(rect_image_pos.x() + rect_image_rect.width())] = 0

        image_component_array = image_component_array * mask
        return image_component_array


    def convert_component_to_qimage(self, component):
        """
        Converts a Fourier component (2D array) to a QImage for display.
        """
        component = (component / np.max(component) * 255).astype(np.uint8)
        height, width = component.shape
        bytes_per_line = component.strides[0]
        return QtGui.QImage(component.data, width, height, bytes_per_line, QtGui.QImage.Format_Grayscale8)


    def get_scene_for_frame(self, frame):
        if frame == 1:
            return self.fourierimage1
        elif frame == 2:
            return self.fourierimage2
        elif frame == 3:
            return self.fourierimage3
        elif frame == 4:
            return self.fourierimage4
        else:
            raise ValueError(f"Invalid frame number: {frame}")
    

    def addResizableRectangle(self, scene,image_component,w,h,inner_rect):
        width = image_component.width()*(w)*0.01
        height = image_component.height()*(h)*0.01
        rect_item = QGraphicsRectItem(0, 0, width, height)

        rect_center_x = (image_component.width() - rect_item.rect().width()) / 2
        rect_center_y = (image_component.height() - rect_item.rect().height()) / 2
        rect_item = QGraphicsRectItem(0, 0, width, height)
        rect_item.setPen(QPen(Qt.yellow))  # Set pen color to yellow
        brush = QBrush(QColor(255, 255, 0, 50))
        rect_item.setBrush(brush)
        rect_item.setPos(rect_center_x, rect_center_y)
        scene.addItem(rect_item)
        if not inner_rect.isChecked():
            brush = QBrush(QColor(0, 0, 0, 50))
            rect_item.setBrush(brush)
            rect_item.setPos(rect_center_x, rect_center_y)
            scene.addItem(rect_item)
            overlay_path = QPainterPath()
            overlay_path.addRect(0, 0, image_component.width(), image_component.height())
            rect_path = QPainterPath()
            rect_path.addRect(rect_center_x, rect_center_y, width, height)
            # Subtract rect_path from overlay_path
            overlay_path -= rect_path
            # Create a QGraphicsPathItem for the resulting path (difference)
            difference_item = scene.addPath(overlay_path, QPen(Qt.NoPen), QBrush(QColor(255, 255, 0, 50)))
        return rect_item



    def apply_region(self, value):
        """
        Applies the region mask to the current Fourier component based on the rectangle.
        The region is adjusted using the region_selector slider.
        """
        for frame in range(1, 5):  # Loop through all frames (1-4)
            if self.current_images[frame - 1] is not None:  # Ensure image is loaded for the frame
                # Update Fourier component for the current frame
                self.update_ft_component(frame - 1)

                # Get the image data and scene for the frame
                img_data = self.current_images[frame - 1]
                scene = self.get_scene_for_frame(frame)  # Retrieve the scene for the current frame

                # Add a resizable rectangle to the scene
                if self.out_region_radioButton.isChecked() or self.in_region_radioButton.isChecked():
                    rect_item = self.addResizableRectangle(
                        scene,
                        self.convert_component_to_qimage(img_data),  # Convert the image component
                        value, 
                        value,
                        self.in_region_radioButton
                    )
                    self.masked_img_comp = self.extractRegion(rect_item, self.convert_component_to_qimage(img_data), img_data, self.in_region_radioButton)


    def extractRegion(self, rect_item, image_component, image_component_array, inner_region_selected):
        image_component = QGraphicsPixmapItem(QPixmap.fromImage(image_component))
        rect_scene_pos = rect_item.scenePos()
        rect_scene_rect = rect_item.rect()
        rect_image_pos = image_component.mapFromScene(rect_scene_pos)
        rect_image_rect = image_component.mapFromScene(rect_scene_rect).boundingRect()

        if inner_region_selected.isChecked():
            mask = np.zeros_like(image_component_array)
            mask[int(rect_image_pos.y()):int(rect_image_pos.y() + rect_image_rect.height()),
                int(rect_image_pos.x()):int(rect_image_pos.x() + rect_image_rect.width())] = 1
        else:
            mask = np.ones_like(image_component_array)
            mask[int(rect_image_pos.y()):int(rect_image_pos.y() + rect_image_rect.height()),
            int(rect_image_pos.x()):int(rect_image_pos.x() + rect_image_rect.width())] = 0

        image_component_array = image_component_array * mask
        return image_component_array


    def convert_component_to_qimage(self, component):
        """
        Converts a Fourier component (2D array) to a QImage for display.
        """
        component = (component / np.max(component) * 255).astype(np.uint8)
        height, width = component.shape
        bytes_per_line = component.strides[0]
        return QtGui.QImage(component.data, width, height, bytes_per_line, QtGui.QImage.Format_Grayscale8)


    def get_scene_for_frame(self, frame):
        if frame == 1:
            return self.fourierimage1
        elif frame == 2:
            return self.fourierimage2
        elif frame == 3:
            return self.fourierimage3
        elif frame == 4:
            return self.fourierimage4
        else:
            raise ValueError(f"Invalid frame number: {frame}")
    

    def addResizableRectangle(self, scene,image_component,w,h,inner_rect):
        width = image_component.width()*(w)*0.01
        height = image_component.height()*(h)*0.01
        rect_item = QGraphicsRectItem(0, 0, width, height)

        rect_center_x = (image_component.width() - rect_item.rect().width()) / 2
        rect_center_y = (image_component.height() - rect_item.rect().height()) / 2
        rect_item = QGraphicsRectItem(0, 0, width, height)
        rect_item.setPen(QPen(Qt.yellow))  # Set pen color to yellow
        brush = QBrush(QColor(255, 255, 0, 50))
        rect_item.setBrush(brush)
        rect_item.setPos(rect_center_x, rect_center_y)
        scene.addItem(rect_item)
        if not inner_rect.isChecked():
            brush = QBrush(QColor(0, 0, 0, 50))
            rect_item.setBrush(brush)
            rect_item.setPos(rect_center_x, rect_center_y)
            scene.addItem(rect_item)
            overlay_path = QPainterPath()
            overlay_path.addRect(0, 0, image_component.width(), image_component.height())
            rect_path = QPainterPath()
            rect_path.addRect(rect_center_x, rect_center_y, width, height)
            # Subtract rect_path from overlay_path
            overlay_path -= rect_path
            # Create a QGraphicsPathItem for the resulting path (difference)
            difference_item = scene.addPath(overlay_path, QPen(Qt.NoPen), QBrush(QColor(255, 255, 0, 50)))
        return rect_item


    ############### PART B ###################

    def update_radio_button_text(self, checked):
        if checked:
            self.array_type = "linear"
            self.curvature_angle_previous = self.curvature_angle
            self.curvature_angle = 0
            self.linear_radio_button.setText("Linear")
            self.curvature_slider.hide()
            self.curvature_lcd.hide()
        else:
            self.array_type = "curved"
            self.curvature_angle = getattr(self, 'curvature_angle_previous', 0)
            self.linear_radio_button.setText("Curved")
            self.curvature_slider.show()
            self.curvature_lcd.show()
        self.beam_forming()

    def update_transmitter_count(self, count):
        print(f"no transmitters updated: {count}")
        self.num_transmitters = count
        self.frequencies = [self.frequencies[0]] * count
        self.phases = [self.phases[0]] * count
        self.beam_forming()

    def update_frequency(self, value):
        print(f"Frequency updated: {value}")
        self.frequencies = [value] * self.num_transmitters
        self.frequency_lcd.display(value)
        self.beam_forming()

    def update_phase(self, value):
        print(f"Phase updated: {value}")
        self.phases = [value] * self.num_transmitters
        self.phase_lcd.display(value)
        self.beam_forming()

    def update_curvature_angle(self, value):
        print(f"curved angle updated: {value}")
        self.curvature_angle = value
        self.curvature_lcd.display(value)
        self.beam_forming()

    def update_array_position(self, value):
        print(f"Array position updated: {value}")
        # Update both X and Y positions to the same value
        self.array_position = [value, value]
        self.position_lcd.display(value)
        self.beam_forming()

    def beam_forming(self):
        print(f"self.frequencies updated: {self.frequencies}")
        print(f"self.phases updated: {self.phases}")
        print(f"self.array_type updated: {self.array_type}")
        print(f"self.curvature_angle updated: {self.curvature_angle}")

        visualizer = Visualizer()
        visualizer.set_frequencies(self.frequencies)
        visualizer.set_phases(self.phases)
        visualizer.set_array_type(self.array_type, self.curvature_angle)
        visualizer.set_position_offset(self.array_position[0], self.array_position[1])

        # Generate and display the plots
        field_map_fig = visualizer.plot_field_map(
            num_transmitters=self.num_transmitters,
            element_spacing=self.element_spacing,
            frequency=self.frequencies[0],
            phases=self.phases,
            curvature_angle=self.curvature_angle,
        )

        beam_pattern_fig = visualizer.plot_beam_pattern_polar(
            num_transmitters=self.num_transmitters,
            element_spacing=self.element_spacing,
            frequency=self.frequencies[0],
            phases=self.phases,
            curvature_angle=self.curvature_angle,
        )
        
        self.display_plot(self.beam_map_view, field_map_fig)
        self.display_plot(self.beam_plot_view, beam_pattern_fig)

    def display_plot(self, widget, figure):
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        from PyQt5.QtWidgets import QVBoxLayout

        if widget.layout() is None:
            widget.setLayout(QVBoxLayout())

        layout = widget.layout()
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

        canvas = FigureCanvas(figure)
        layout.addWidget(canvas)
        layout.setAlignment(QtCore.Qt.AlignCenter)

    def update_scenario_parameters(self):
        scenario = self.scenario_combobox.currentText()
        parameters = scenarios.ScenarioParameters()
        if scenario == "5G":
            parameters.update_parameters("5G")
            parameters.display_parameters()
        elif scenario == "Ultrasound":
            parameters.update_parameters("Ultrasound")
            parameters.display_parameters()
        elif scenario == "Tumor Ablation":
            parameters.update_parameters("Tumor Ablation")
            parameters.display_parameters()
        else:
            parameters.update_parameters("Custom")
            parameters.display_parameters()
        
        self.frequency_slider.setValue(parameters.frequency)
        self.phase_slider.setValue(parameters.phase)
        self.curvature_slider.setValue(parameters.curvature_angle)
        self.position_slider.setValue(parameters.position_between_transmitters)
        self.no_transmitters_spinbox.setValue(parameters.num_transmitters)

        print(f"Scenario updated: {scenario}")
        print(f"self.frequencies updated: {self.frequencies}")
        print(f"self.phases updated: {self.phases}")
        print(f"self.array_type updated: {self.array_type}")
        print(f"self.curvature_angle updated: {self.curvature_angle}")

        self.beam_forming()

# Entry point of the application
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
