from PyQt5 import QtWidgets, QtGui, QtCore, uic   # Added uic import
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene, QMessageBox
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
from regionSelector import ResizableRectangle
from fourier_components import FourierComponents


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('task4.ui', self)
        
        
        self.min_width = 0
        self.min_height = 0
        self.used_height = 657
        self.used_width = 458

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

        self.fourier_components = FourierComponents(self.Gimage1, self.current_images,
                                                   self.Fourier_comboBox_1, self.Fourier_comboBox_2,
                                                   self.Fourier_comboBox_3, self.Fourier_comboBox_4,
                                                   self.weight_1, self.weight_2, self.weight_3, self.weight_4, self.fourierimage1, self.fourierimage2, self.fourierimage3, self.fourierimage4)

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

        self.image1_loaded = False 
        self.image2_loaded = False 
        self.image3_loaded = False 
        self.image4_loaded = False 

        # # Add selection rectangles to Fourier scenes
        self.linked_rectangles = []
        self.rectangle = ResizableRectangle(x=10, y=10, width=245, height=130)
        self.rect1 = ResizableRectangle(width=200, height=140)
        self.rect2 = ResizableRectangle(x=10, y=10, width=245, height=130)
        self.rect3 = ResizableRectangle(x=10, y=10, width=245, height=130)
        self.rect4 = ResizableRectangle(x=10, y=10, width=245, height=130)
        self.rects = [self.rect1, self.rect2, self.rect3,self.rect4]
        ResizableRectangle.center_on_images(self.min_width, self.min_height)
        # self.rect1.geometryChanged.connect(self.handle_region_change)

        # Inside your main setup method (e.g., __init__ or a setupUi wrapper)
        self.in_region_radioButton.toggled.connect(self.handle_region_change)
        self.out_region_radioButton.toggled.connect(self.handle_region_change)


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
        self.curvature_angle_label = self.findChild(QtWidgets.QLabel, "curvature_angle_label")
        self.beam_position_slider = self.findChild(QtWidgets.QSlider, "beam_position_slider")
        self.position_lcd = self.findChild(QtWidgets.QLCDNumber, "position_lcd")
        self.beam_position_y_slider = self.findChild(QtWidgets.QSlider, "position_y_slider")
        self.position_y_lcd = self.findChild(QtWidgets.QLCDNumber, "position_y_lcd")
        self.curvature_unit_label = self.findChild(QtWidgets.QLabel, "label_12")
        self.spacing_slider = self.findChild(QtWidgets.QSlider, "spacing_slider")
        self.spacing_lcd = self.findChild(QtWidgets.QLCDNumber, "spacing_lcd")


        self.beam_map_view = self.findChild(QtWidgets.QWidget, "beam_map")
        self.beam_plot_view = self.findChild(QtWidgets.QWidget, "beam_plot")
        self.scenario_combobox = self.findChild(QtWidgets.QComboBox, "comboBox_Open_scenario")

        # Initialize parameters
        self.num_transmitters = 2
        self.frequencies = [1000000000] * self.num_transmitters  # Default frequency for each transmitter
        self.phases = [0] * self.num_transmitters  # Default phase for each transmitter
        self.array_type = "curved"  # Default to curved
        self.curvature_angle = 30  # Default curvature angle
        self.element_spacing = 0.5  # Default element spacing
        self.array_position = [0, 0]  # Default position of the array

        # Set the initial state of radio button
        self.linear_radio_button.setChecked(False)
        self.update_radio_button_text(self.linear_radio_button.isChecked())
        self.linear_radio_button.toggled.connect(self.update_radio_button_text)
        self.scenario_combobox.currentText() == "Open Scenario"
        self.update_scenario_parameters()

        # Connect UI elements to methods
        self.frequency_slider.setMinimum(100000000)
        self.frequency_slider.setMaximum(2000000000)
        self.frequency_slider.setSingleStep(10000000)  # Step size
        self.frequency_slider.valueChanged.connect(self.update_frequency)
        self.phase_slider.setMinimum(-180)
        self.phase_slider.setMaximum(180)
        self.phase_slider.setValue(0)
        self.phase_slider.valueChanged.connect(self.update_phase)
        self.curvature_slider.setMinimum(1)
        self.curvature_slider.setMaximum(180)
        self.curvature_slider.valueChanged.connect(self.update_curvature_angle)
        self.no_transmitters_spinbox.setMinimum(2)
        self.no_transmitters_spinbox.setMaximum(100)
        self.no_transmitters_spinbox.valueChanged.connect(self.update_transmitter_count)
        self.beam_position_slider.setMinimum(-10)
        self.beam_position_slider.setMaximum(10)
        self.beam_position_slider.setSingleStep(1)
        self.beam_position_slider.valueChanged.connect(self.update_array_Xposition)
        self.beam_position_y_slider.setMinimum(0)
        self.beam_position_y_slider.setMaximum(10)
        self.beam_position_y_slider.setSingleStep(1)
        self.beam_position_y_slider.valueChanged.connect(self.update_array_Yposition)

        self.spacing_slider.setMinimum(1)
        self.spacing_slider.setMaximum(200)
        self.spacing_slider.setSingleStep(1)
        self.spacing_slider.setValue(50)
        self.spacing_lcd.setDigitCount(3)
        self.spacing_lcd.display(0.5)
        self.spacing_slider.valueChanged.connect(self.update_spacing)

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
                self.fourier_components.compute_ft_components(0)
                self.fourier_components.update_ft_component(0)
                self.add_rectangle_to_frame(0) 
                self.image1_loaded = True  

            elif frame == 2:
                self.scene2.clear()
                pixmap = pixmap.scaled(self.min_width, self.min_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene2.addPixmap(pixmap)
                self.scene2.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.image2.fitInView(self.scene2.sceneRect(), QtCore.Qt.KeepAspectRatio)
                self.fourier_components.compute_ft_components(1)
                self.fourier_components.update_ft_component(1)
                self.add_rectangle_to_frame(1) 
                self.image2_loaded = True

            elif frame == 3:
                self.scene3.clear()
                pixmap = pixmap.scaled(self.min_width, self.min_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene3.addPixmap(pixmap)
                self.scene3.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.image3.fitInView(self.scene3.sceneRect(), QtCore.Qt.KeepAspectRatio)
                self.fourier_components.compute_ft_components(2)
                self.fourier_components.update_ft_component(2)
                self.add_rectangle_to_frame(2) 
                self.image3_loaded = True

            elif frame == 4:
                self.scene4.clear()
                pixmap = pixmap.scaled(self.min_width, self.min_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene4.addPixmap(pixmap)
                self.scene4.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.image4.fitInView(self.scene4.sceneRect(), QtCore.Qt.KeepAspectRatio)
                self.fourier_components.compute_ft_components(3)
                self.fourier_components.update_ft_component(3)
                self.add_rectangle_to_frame(3) 
                self.image4_loaded = True
            self.resize_images()   
    
    def add_rectangle_to_frame(self, frame):
        print("self.scene1.sceneRect():",self.image1.width()) 
        if frame == 0:
            currentFourierImage = self.fourierimage1
            print("frame1")
        elif frame == 1:
            currentFourierImage = self.fourierimage2
            print("frame2")
        elif frame == 2:
            currentFourierImage = self.fourierimage3
            self.update_weight(2, self.weight_3.value())
            print("frame3")
        elif frame == 3:
            currentFourierImage = self.fourierimage4
            self.update_weight(3, self.weight_4.value()) 

        # if selected_component in self.ft_components[frame]:
        print("def add_rectangle_to_frame(self, frame):**********")
            
        self.rect1 = ResizableRectangle(x=10, y=10, width=245, height=130)
        self.rect1.linked_rectangles = self.rects  # Share the same list
        self.rects[frame] = self.rect1
        currentFourierImage.addItem(self.rect1)

                
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
                
                self.used_width = self.loaded_images[i].width()
                self.used_height = self.loaded_images[i].height()
                print("self.used_width: ",self.used_width)
                
                print(f"Image {i} resized to {self.min_width}x{self.min_height}")
                # to resize the ft image also     
                self.fourier_components.update_ft_component(i)


    def change_choices_combobox(self):
        # This method is now in the FourierComponents class
        self.fourier_components.change_choices_combobox(self.magnitude_phase, self.real_imaginary)
                    
    
    def change_output_location(self):
        mixed_image = self.compute_inverse_ft_components()
        if self.output1.isChecked():
            self.display_output_image(self.output_mixer1, self.scene_output1, mixed_image)  
        elif self.output2.isChecked():
            self.display_output_image(self.output_mixer2, self.scene_output2, mixed_image)                                
    
    
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

            for i in range(len(self.fourier_components.ft_components)):
                if self.current_images[i] is not None:
                    x_min = self.rects[i].x_min    # Leftmost x
                    x_max = self.rects[i].x_max   # Rightmost x
                    y_min = self.rects[i].y_min     # Topmost y
                    y_max = self.rects[i].y_max  # Bottommost y
                    print(f"self.rectangle in inverse ft: {self.rectangle}")
                    print("x_min, y_min:", x_min, y_min, "x_max, y_max", x_max, y_max)
                    print("self.min_width:", self.min_width, "self.min_height", self.min_height)

                    # Ensure bounds are within the image size
                    x_min, x_max = max(0, x_min), min(self.used_width, x_max)
                    y_min, y_max = max(0, y_min), min(self.used_height, y_max)
                    if self.in_region_radioButton.isChecked():
                        mask = np.zeros(( self.used_width,self.used_height), dtype=np.uint8)
                        mask[y_min:y_max, x_min:x_max] = 1
                    else:
                        mask = np.ones((self.used_width,self.used_height), dtype=np.uint8)
                        mask[y_min:y_max, x_min:x_max] = 0
                        
                    mask = cv2.resize(mask, (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)
                    resized_magnitude = cv2.resize(self.fourier_components.ft_components[i]["FT Magnitude"], (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)
                    resized_phase = cv2.resize(self.fourier_components.ft_components[i]["FT Phase"], (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)
                    # ft_phase_sum = np.zeros_like(resized_phase, dtype=np.complex128)
                    ft_magnitude_sum += resized_magnitude * magnitude_weights[i] 
                    # ft_phase_sum += np.exp(1j * resized_phase) * phase_weights[i]
                    ft_phase_sum += resized_phase * phase_weights[i]
            # Reconstruct using magnitude and phase
            # reconstructed_ft = np.multiply(np.expm1(ft_magnitude_sum), np.exp(1j * np.angle(ft_phase_sum)))
            reconstructed_ft = np.multiply(np.expm1(ft_magnitude_sum), np.exp(1j * ft_phase_sum))
            reconstructed_ft *= mask
            reconstructed_image =  np.abs(np.fft.ifft2(np.fft.ifftshift(reconstructed_ft)))
            # reconstructed_image *= mask

        else:
            ft_real_sum = np.zeros((self.min_height, self.min_width))
            ft_imaginary_sum = np.zeros((self.min_height, self.min_width))

            rect_bounds = self.rectangle.sceneBoundingRect()
            x_min, y_min = int(rect_bounds.left()), int(rect_bounds.top())
            x_max, y_max = int(rect_bounds.right()), int(rect_bounds.bottom())
            print(f"self.rectangle in inverse ft: {self.rectangle}")

            for i in range(len(self.fourier_components.ft_components)):
                if self.current_images[i] is not None:
                    x_min = self.rects[i].x_min    # Leftmost x
                    x_max = self.rects[i].x_max   # Rightmost x
                    y_min = self.rects[i].y_min     # Topmost y
                    y_max = self.rects[i].y_max  # Bottommost y
                    print(f"self.rectangle in inverse ft: {self.rectangle}")
                    print("x_min, y_min:", x_min, y_min, "x_max, y_max", x_max, y_max)
                    print("self.min_width:", self.min_width, "self.min_height", self.min_height)
                    # Ensure bounds are within the image size
                    x_min, x_max = max(0, x_min), min(self.used_width, x_max)
                    y_min, y_max = max(0, y_min), min(self.used_height, y_max)
                    if self.in_region_radioButton.isChecked():
                        mask = np.zeros(( self.used_width,self.used_height), dtype=np.uint8)
                        mask[y_min:y_max, x_min:x_max] = 1
                    else:
                        mask = np.ones((self.used_width,self.used_height), dtype=np.uint8)
                        mask[y_min:y_max, x_min:x_max] = 0
                        
                    mask = cv2.resize(mask, (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)
                    resized_real = self.fourier_components.ft_components[i]["FT Real"].reshape(self.min_height, self.min_width)
                    resized_imaginary = self.fourier_components.ft_components[i]["FT Imaginary"].reshape(self.min_height, self.min_width)
                    ft_real_sum += resized_real * real_weights[i] * mask
                    ft_imaginary_sum += resized_imaginary * imaginary_weights[i] * mask

            # Reconstruct using real and imaginary parts
            mixed_image = np.fft.ifft2(ft_real_sum + 1j * ft_imaginary_sum)
            reconstructed_image = np.abs(mixed_image)

        # Normalize to range [0, 255]
        if reconstructed_image is not None:
            max_val = np.max(reconstructed_image)
            reconstructed_image = (255 * (reconstructed_image / max_val)).astype(np.uint8) if max_val > 0 else np.zeros_like(reconstructed_image, dtype=np.uint8)

        return reconstructed_image

    def handle_region_change(self):
        if self.in_region_radioButton.isChecked():
            print("Processing inner region.")
        elif self.out_region_radioButton.isChecked():
            print("Processing outer region.")
        self.change_output_location()


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
            self.fourier_components.compute_ft_components(frame_index)
            self.fourier_components.update_ft_component(frame_index)
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


    
    ############### PART B ###################

    def update_radio_button_text(self, checked):
        if checked:
            self.array_type = "linear"
            self.curvature_angle_previous = self.curvature_angle
            self.curvature_angle = 0
            self.linear_radio_button.setText("Linear")
            self.curvature_slider.hide()
            self.curvature_lcd.hide()
            self.curvature_angle_label.hide()
            self.curvature_unit_label.hide()
        else:
            self.array_type = "curved"
            self.curvature_angle = getattr(self, 'curvature_angle_previous', 30)
            self.linear_radio_button.setText("Curved")
            self.curvature_slider.show()
            self.curvature_lcd.show()
            self.curvature_angle_label.show()
            self.curvature_unit_label.show()
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
        self.frequency_lcd.display(value//1000000)
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

    def update_array_Xposition(self, value):
        print(f"Array position x updated: {value}")
        self.array_position[0] = [value]
        self.position_lcd.display(value)
        self.beam_forming()

    def update_array_Yposition(self,value):
        print(f"Array position y updated: {value}")
        self.array_position[1] = [value]
        self.position_y_lcd.display(value)
        self.beam_forming()

    def update_spacing(self, value):
        spacing = value / 100.0
        self.element_spacing = spacing
        print(f"Element spacing updated: {spacing:.2f}")
        self.spacing_lcd.setDigitCount(4)  # Ensure enough space for decimal display
        self.spacing_lcd.display(f"{spacing:.2f}")  # Show decimal value
        self.beam_forming()

    def beam_forming(self):
        visualizer = Visualizer()
        visualizer.set_frequencies(self.frequencies)
        visualizer.set_phases(self.phases)
        visualizer.set_array_type(self.array_type, self.curvature_angle)
        visualizer.set_position_offset(self.array_position[0], self.array_position[1])
        visualizer.set_element_spacing(self.element_spacing)
        
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
        elif scenario == "Airborne Radar":
            parameters.update_parameters("Airborne Radar")
            parameters.display_parameters()
        elif scenario == "Tumor Ablation":
            parameters.update_parameters("Tumor Ablation")
            parameters.display_parameters()
        elif scenario == "Ultrasound":
            parameters.update_parameters("Ultrasound")
            parameters.display_parameters()
        else:
            parameters.update_parameters("Custom")
            parameters.display_parameters()
        
        self.array_type = parameters.array_geometry
        if self.array_type == "linear":
            self.linear_radio_button.setChecked(True)
        else:
            self.linear_radio_button.setChecked(False)  
        self.update_radio_button_text(self.linear_radio_button.isChecked())
        self.frequency_slider.setValue(parameters.frequency)
        self.phase_slider.setValue(parameters.phase)
        self.curvature_slider.setValue(parameters.curvature_angle)
        self.no_transmitters_spinbox.setValue(parameters.num_transmitters)
        self.spacing_slider.setValue(int(parameters.position_between_transmitters * 10))
        self.beam_position_slider.setValue(0)
        self.beam_position_y_slider.setValue(0)
        
       

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