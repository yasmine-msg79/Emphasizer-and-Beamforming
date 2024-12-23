from PyQt5 import QtWidgets, QtGui, QtCore, uic   # Added uic import
import sys
from PyQt5.QtGui import *
import numpy as np
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtGui import QImage, QPixmap
import scenarios
from visualizer import Visualizer
from PIL import Image
from regionSelector import ResizableRectangle

class Image:
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
                self.update_ft_component(i)

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
