from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt

def display_output_image(self, label, mixed_image):
    # Get image dimensions
    height, width = mixed_image.shape
    bytes_per_line = width  # For grayscale, this is just the width

    # Convert NumPy array to QImage
    q_image = QImage(mixed_image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)

    # Create a scene for displaying the image
    scene_out = QGraphicsScene()

    # Create a pixmap item and add it to the scene
    pixmap_item = QGraphicsPixmapItem(QPixmap.fromImage(q_image))
    scene_out.addItem(pixmap_item)

    # Set the scene on the label and fit the image to the view
    label.setScene(scene_out)
    label.fitInView(pixmap_item, Qt.KeepAspectRatio)
import numpy as np

# Example matrix
mixed_image = np.array([[ 63,  54,  52,  58,  66, 111],
                        [168,  52,  94,  46,  46,  55],
                        [ 73,  93, 105,  74,  62,  56],
                        [181, 178, 177, 135, 172, 192],
                        [201, 197, 186,  73,  76,  91],
                        [125, 161, 181,  76,  75,  73]])

# Assuming 'label' is a QGraphicsView object
self.display_output_image(label, mixed_image)
