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
import beamPlot
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

        ################# PART B #########################
        self.linear_radio_button = self.findChild(QtWidgets.QRadioButton, "linear_radio_button_3")
        self.curvature_angle_spinbox = self.findChild(QtWidgets.QDoubleSpinBox, "doubleSpinBox_curvature_angle_3")
        self.curvature_angle_label = self.findChild(QtWidgets.QLabel, "label_15")
        self.no_transmitters_spinbox = self.findChild(QtWidgets.QSpinBox, "spinBox_No_transmitters_3")
        self.frequency_phase_table_2 = self.findChild(QtWidgets.QTableWidget, "frequency_phase_table_2")

        # Initialize parameters
        self.frequencies = []
        self.phases = []
        self.element_spacing = 0.5  # Wavelength units
        self.array_type = "curved"  # Default array type
        self.curvature_angle = 0.0  # Default curvature angle (in degrees)


        # Set the initial state
        self.linear_radio_button.setChecked(False)  
        self.linear_radio_button.setText("Curved")  

        self.update_radio_button_text(self.linear_radio_button.isChecked())
        self.linear_radio_button.toggled.connect(self.update_radio_button_text)

        # Connect spinbox signal for changing transmitter count
        self.no_transmitters_spinbox.valueChanged.connect(self.update_transmitter_rows)
        self.curvature_angle_spinbox.valueChanged.connect(self.update_curvature_angle)

        # Set up the table
        self.frequency_phase_table_2.setColumnCount(2)
        self.frequency_phase_table_2.setHorizontalHeaderLabels(["Frequency", "Phase"])
        self.frequency_phase_table_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.frequency_phase_table_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.frequency_phase_table_2.verticalHeader().setDefaultSectionSize(60)

        self.beam_map_view = self.findChild(QtWidgets.QWidget, "beam_map")
        self.beam_plot_view = self.findChild(QtWidgets.QWidget, "beam_plot")

        # Initialize phased array properties
        self.num_transmitters = 3
        self.frequencies = [1000] * self.num_transmitters  # Default frequency for each transmitter
        self.phases = [0] * self.num_transmitters  # Default phase for each transmitter

        # self.beam_forming()

        # Create spinboxes for the transmitters
        for row in range(self.num_transmitters):
            self.add_custom_widget(row, 0, "frequency")
            self.add_custom_widget(row, 1, "phase")

        
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
                      
            image_calculations = Image.open(file_name).convert('L')
            resize_image_calculations = image_calculations.resize((self.min_width ,self.min_height))
            self.current_images[frame - 1] = resize_image_calculations
            ptr = image.bits()
            ptr.setsize(self.min_width * self.min_height)
            if frame == 1:
                self.scene.clear()
                pixmap = pixmap.scaled(self.image1.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene.addPixmap(pixmap)
                self.scene.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.image1.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
                # self.current_images[frame - 1] = np.array(ptr).reshape(self.min_height, self.min_width)
                self.compute_ft_components(0)
                self.update_ft_component(0)
            
            elif frame == 2:
                self.scene2.clear()
                pixmap = pixmap.scaled(self.image2.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene2.addPixmap(pixmap)
                self.scene2.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.image2.fitInView(self.scene2.sceneRect(), QtCore.Qt.KeepAspectRatio)
                # self.current_images[frame - 1] = np.array(ptr).reshape(self.min_height, self.min_width)
                self.compute_ft_components(1)
                self.update_ft_component(1)
            
            elif frame == 3:
                self.scene3.clear()
                pixmap = pixmap.scaled(self.image3.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene3.addPixmap(pixmap)
                self.scene3.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.image3.fitInView(self.scene3.sceneRect(), QtCore.Qt.KeepAspectRatio)
                # self.current_images[frame - 1] = np.array(ptr).reshape(self.min_height, self.min_width)
                self.compute_ft_components(2)
                self.update_ft_component(2)    
            
            elif frame == 4:
                self.scene4.clear()
                pixmap = pixmap.scaled(self.image4.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.scene4.addPixmap(pixmap)
                self.scene4.setSceneRect(QtCore.QRectF(pixmap.rect()))
                self.image4.fitInView(self.scene4.sceneRect(), QtCore.Qt.KeepAspectRatio)
                # self.current_images[frame - 1] = np.array(ptr).reshape(self.min_height, self.min_width)
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
                    resized_magnitude = cv2.resize(self.ft_components[i]["FT Magnitude"], (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)
                    resized_phase = cv2.resize(self.ft_components[i]["FT Phase"], (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)

                    # resized_magnitude = self.ft_components[i]["FT Magnitude"].reshape(self.min_height, self.min_width)
                    # resized_magnitude = self.ft_components[i]["FT Magnitude"][:self.min_height, :self.min_width]
                    # resized_magnitude = cv2.resize(self.ft_components[i]["FT Magnitude"], (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)
                    # resized_phase = self.ft_components[i]["FT Phase"].reshape(self.min_height, self.min_width)

                    ft_magnitude_sum += resized_magnitude * magnitude_weights[i]
                    ft_phase_sum += resized_phase * phase_weights[i]

            # Reconstruct using magnitude and phase
            reconstructed_ft = np.multiply(np.expm1(ft_magnitude_sum), np.exp(1j * ft_phase_sum))
            # mixed_image = np.fft.ifft2(np.fft.ifftshift(reconstructed_ft))
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

        # Save the reconstructed image as a JPEG
        # self.save_image_as_jpeg(reconstructed_image, "reconstructed_image.jpg")
        # return ( self.current_images[0] - reconstructed_image)
        
        # return ( self.current_images[0] - reconstructed_image)
        return reconstructed_image


    def save_image_as_jpeg(self, image_matrix, filename):
        """
        Save a NumPy matrix as a JPEG image.

        Args:
            image_matrix (np.ndarray): Grayscale image matrix.
            filename (str): The file name for the saved image.
        """
        success = cv2.imwrite(filename, image_matrix)
        if success:
            QtWidgets.QMessageBox.information(self, "Success", f"Image saved successfully as {filename}")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Failed to save the image.")


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
        if label == self.output_mixer1:
            scene = self.scene_output1 
            self.scene_output1.clear()
        else:
            scene = self.scene_output2 
            self.scene_output2.clear() 
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





    ############### PART B ###################

    def update_transmitter_rows(self):
        """
        Updates the number of rows in the frequency and phase table based on the transmitter count.
        """
        count = self.no_transmitters_spinbox.value()
        current_rows = self.frequency_phase_table_2.rowCount()

        # Add or remove rows to match the transmitter count
        while count > current_rows:
            self.add_table_row()
            current_rows += 1
        while count < current_rows:
            self.frequencies.pop()
            self.phases.pop()
            self.frequency_phase_table_2.removeRow(current_rows - 1)
            current_rows -= 1

        # Recalculate beamforming after updating rows
        self.beam_forming()

    def add_table_row(self):
        """
        Adds a new row with default widgets for frequency and phase.
        """
        row_position = self.frequency_phase_table_2.rowCount()
        self.frequency_phase_table_2.insertRow(row_position)

        # Ensure the frequencies and phases lists have room for the new row
        self.frequencies.append(1000)  # Default frequency
        self.phases.append(0.0)  # Default phase

        # Create new spin boxes for frequency and phase
        freq_spinbox = QSpinBox()
        freq_spinbox.setMinimum(1)
        freq_spinbox.setMaximum(10000)
        freq_spinbox.setValue(self.frequencies[row_position])  # Default frequency value
        freq_spinbox.valueChanged.connect(lambda value, row=row_position: self.update_parameters(row, "frequency", value))

        phase_spinbox = QDoubleSpinBox()
        phase_spinbox.setMinimum(-180)
        phase_spinbox.setMaximum(180)
        phase_spinbox.setValue(self.phases[row_position])  # Default phase value
        phase_spinbox.setSingleStep(0.1)
        phase_spinbox.valueChanged.connect(lambda value, row=row_position: self.update_parameters(row, "phase", value))

        # Add the frequency spin box to the first column
        freq_layout = QVBoxLayout()
        freq_layout.addWidget(freq_spinbox)
        freq_layout.setAlignment(Qt.AlignCenter)
        freq_widget = QWidget()
        freq_widget.setLayout(freq_layout)
        self.frequency_phase_table_2.setCellWidget(row_position, 0, freq_widget)

        # Add the phase spin box to the second column
        phase_layout = QVBoxLayout()
        phase_layout.addWidget(phase_spinbox)
        phase_layout.setAlignment(Qt.AlignCenter)
        phase_widget = QWidget()
        phase_widget.setLayout(phase_layout)
        self.frequency_phase_table_2.setCellWidget(row_position, 1, phase_widget)

    def update_radio_button_text(self, checked):
        """
        Updates the UI based on the radio button state.
        If checked, the radio button text changes to 'Curved', and curvature angle controls are shown.
        If unchecked, the radio button text changes to 'Linear', and curvature angle controls are hidden.
        """
        if checked:
            self.linear_radio_button.setText("linear") # Update the label next to the radio button
            self.curvature_angle_label.setVisible(False)  # Show the "Curvature Angle" label
            self.curvature_angle_spinbox.setVisible(False)  # Show the spinbox
        else:
            self.linear_radio_button.setText("curved")  # Update the label next to the radio button
            self.curvature_angle_label.setVisible(True)  # Hide the "Curvature Angle" label
            self.curvature_angle_spinbox.setVisible(True)  # Hide the spinbox


    def add_custom_widget(self, row, col, mode):
        """
        Add a spinbox to the table for either frequency or phase adjustments.
        """
        widget = QtWidgets.QSpinBox() if mode == "frequency" else QtWidgets.QDoubleSpinBox()
        widget.setMinimum(1 if mode == "frequency" else -180)
        widget.setMaximum(10000 if mode == "frequency" else 180)
        widget.setValue(self.frequencies[row] if mode == "frequency" else self.phases[row])

        # Connect signal to update plots dynamically
        widget.valueChanged.connect(lambda value, r=row, c=col, m=mode: self.update_parameters(r, m, value))

        # Add the widget to the corresponding cell in the table
        self.frequency_phase_table_2.setCellWidget(row, col, widget)

    def update_parameters(self, row, mode, value):
        """
        Update parameters based on spinbox changes and regenerate plots.
        """
        if mode == "frequency":
            self.frequencies[row] = value  # Update the frequency for the given transmitter
        elif mode == "phase":
            self.phases[row] = value  # Update the phase for the given transmitter

        # Recalculate and update the plots
        self.beam_forming()

    def beam_forming(self):
        """
        Generate and display updated heatmap and beam profile based on parameters.
        """
        # Create an instance of the Visualizer
        visualizer = Visualizer()

        # Update the visualizer's state
        visualizer.set_frequencies(self.frequencies)
        visualizer.set_phases(self.phases)
        visualizer.set_array_type(self.array_type, self.curvature_angle)

        # Generate updated plots
        heatmap_fig = visualizer.plot_beam_pattern()
        phase_mag_fig = visualizer.plot_phase_magnitude()

        # Display the updated plots
        self.display_plot(self.beam_plot_view, heatmap_fig)
        self.display_plot(self.beam_map_view, phase_mag_fig)

    def display_plot(self, widget, figure):
        """
        Utility to render a matplotlib plot into a QWidget.
        """
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        from PyQt5.QtWidgets import QVBoxLayout

        # Ensure the widget has a layout
        if widget.layout() is None:
            widget.setLayout(QVBoxLayout())

        # Clear any existing widgets in the layout
        layout = widget.layout()
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

        # Create a new FigureCanvas and add it to the layout
        canvas = FigureCanvas(figure)
        layout.addWidget(canvas)
        layout.setAlignment(QtCore.Qt.AlignCenter)
    
    def update_curvature_angle(self, value):
        """
        Updates the curvature angle for the phased array and recalculates the beamforming pattern.
        """
        self.curvature_angle = value  # Update the curvature angle
        self.beam_forming()  # Recalculate the beamforming pattern


# Entry point of the application
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())








    # def beam_forming(self):
    #     # Create an instance of the Visualizer
    #     visualizer = beamPlot.Visualizer()
    #     visualizer.map1 = self.beam_map_view
    #     visualizer.plot1 = self.beam_plot_view

    #     # Generate beam pattern (heatmap)
    #     heatmap_fig = visualizer.plot_beam_pattern()

    #     # Generate phase-magnitude plot
    #     phase_mag_fig = visualizer.plot_phase_magnitude()

    #     # Display the heatmap in beam_plot
    #     self.display_plot(self.beam_plot_view, heatmap_fig)

    #     # Display the phase-magnitude plot in beam_map
    #     self.display_plot(self.beam_map_view, phase_mag_fig)

    # def display_plot(self, widget, figure):
    #     """
    #     Utility to render a matplotlib plot into a QWidget.
        
    #     Parameters:
    #     - widget: The target QWidget where the plot should be displayed.
    #     - figure: The matplotlib figure to be rendered.
    #     """
    #     from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    #     from PyQt5.QtWidgets import QVBoxLayout

    #     # # Clear any existing layout or children in the widget
    #     # for i in reversed(range(widget.layout().count())):
    #     #     widget.layout().itemAt(i).widget().deleteLater()

    #     # Create a new FigureCanvas and add it to the widget
    #     canvas = FigureCanvas(figure)
    #     layout = widget.layout() if widget.layout() else QVBoxLayout(widget)
    #     layout.addWidget(canvas)
    #     layout.setAlignment(QtCore.Qt.AlignCenter)
    #     widget.setLayout(layout)
