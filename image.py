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

class Image():
    def __init__(self):
        super(Image, self).__init__()