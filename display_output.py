# display_manager.py

from PyQt5 import QtGui, QtCore

class DisplayManager:
    def __init__(self, scene_output1, scene_output2, output_mixer1, output_mixer2):
        self.scene_output1 = scene_output1
        self.scene_output2 = scene_output2
        self.output_mixer1 = output_mixer1
        self.output_mixer2 = output_mixer2
        
    def display_output_image(self, label, scene, mixed_image):
        scene.clear()
        height, width = mixed_image.shape
        image_data = mixed_image.tobytes()
        q_image = QtGui.QImage(image_data, width, height, width, QtGui.QImage.Format_Grayscale8)
        pixmap = QtGui.QPixmap.fromImage(q_image)
        pixmap = pixmap.scaled(label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        scene.addPixmap(pixmap)
        scene.setSceneRect(QtCore.QRectF(pixmap.rect()))
        label.fitInView(scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
