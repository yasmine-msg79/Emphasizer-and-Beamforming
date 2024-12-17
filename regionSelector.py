from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QPen, QColor, QPainterPath, QBrush, QPainter, QCursor
from PyQt5.QtCore import Qt, QRectF, QSizeF, QPointF
import numpy as np


class ResizableRectangle(QGraphicsRectItem):
    linked_rectangles = []  # Shared list of linked rectangles

    def __init__(self, x=0, y=0, width=80, height=80):
        super().__init__(x, y, width, height)
        self.setFlags(QGraphicsRectItem.ItemIsMovable | QGraphicsRectItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)

        # Appearance
        self.pen_color = QColor(128, 0, 128)  # Purple border
        self.border_radius = 10
        self.setPen(QPen(self.pen_color, 2))
        self.setBrush(QBrush(QColor(0, 0, 255, 50)))  # Transparent blue fill

        # Resizing behavior
        self.resize_handle_size = 10
        self.resizing = False
        self.cursor_in_resize = False
        ResizableRectangle.linked_rectangles.append(self)  # Add rectangle to shared list
        self.bounding_rect = self.sceneBoundingRect()
        self.x_min = x
        self.x_max = x + width
        self.y_min = y
        self.y_max = y + height

    def hoverMoveEvent(self, event):
        """
        Change cursor when hovering over the resize handle.
        """
        if self._is_in_resize_area(event.pos()):
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))
        super().hoverMoveEvent(event)

    def mousePressEvent(self, event):
        """
        Start resizing if clicking on the resize handle.
        """
        if self._is_in_resize_area(event.pos()):
            self.resizing = True
            self.start_pos = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
        Handle resizing or moving the rectangle.
        """
        if self.resizing:
            delta = event.pos() - self.start_pos
            delta_width = delta.x()
            delta_height = delta.y()

            new_width = max(self.rect().width() + delta_width, self.resize_handle_size)
            new_height = max(self.rect().height() + delta_height, self.resize_handle_size)

            # Notify the scene about geometry change
            self.prepareGeometryChange()

            new_rect = QRectF(self.rect().topLeft(), QSizeF(new_width, new_height))
            self.setRect(new_rect)
            self.start_pos = event.pos()

            # Force the scene to update
            if self.scene():
                self.scene().update()

            # self.sync_with_linked_rectangles()  # Sync changes

            # Debug: Print updated geometry
            print("Rect:", self.rect())
            rect = self.rect()  # Call the rect method to get the QRectF object

            # Now extract the values
            self.x_min = int(rect.x())  # Leftmost x
            self.x_max = int(rect.x() + new_width)  # Rightmost x
            self.y_min = int(rect.y())  # Topmost y
            self.y_max = int(rect.y() + new_height)  # Bottommost y
            print("Classsss///**x_min, y_min:",  self.x_min,  self.y_min, "x_max, y_max",  self.x_max,  self.y_max)  
        else:
            super().mouseMoveEvent(event)


    # def mouseMoveEvent(self, event):
    #     if self.resizing:
    #         delta = event.pos() - self.start_pos
    #         delta_width = delta.x()
    #         delta_height = delta.y()

    #         new_width = max(self.rect().width() + delta_width, self.resize_handle_size)
    #         new_height = max(self.rect().height() + delta_height, self.resize_handle_size)
    #         new_rect = QRectF(self.rect().topLeft(), QSizeF(new_width, new_height))
    #         self.setRect(new_rect)
    #         self.start_pos = event.pos()

    #         self.sync_with_linked_rectangles()  # Sync changes
    #     else:
    #         super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Stop resizing.
        """
        if self.resizing:
            self.resizing = False
            self.setCursor(QCursor(Qt.ArrowCursor))
        super().mouseReleaseEvent(event)


    def _is_in_resize_area(self, pos):
        """
        Determine if the mouse is near the bottom-right corner for resizing.
        """
        rect = self.rect()
        resize_x = rect.right() - self.resize_handle_size
        resize_y = rect.bottom() - self.resize_handle_size
        return resize_x <= pos.x() <= rect.right() and resize_y <= pos.y() <= rect.bottom()
    def update_start_end_points(self):
        """
        Update the start and end points of the rectangle after resizing or movement.
        """
        rect = self.rect()
        self.rect_start = rect.topLeft()
        self.rect_end = rect.bottomRight()

    def extract_region_data(self, image_data, innerRegion):
        """
        Extract the region inside or outside the rectangle from the given image data.
        
        Args:
            image_data (np.ndarray): The image data as a NumPy array.
            mode (str): 'InsideRegion' or 'OutsideRegion' to determine masking behavior.

        Returns:
            cropped_data (np.ndarray): The image data with the mask applied.
        """
        # Get integer bounds
        start_x = int(self.rect_start.x())
        start_y = int(self.rect_start.y())
        end_x = int(self.rect_end.x())
        end_y = int(self.rect_end.y())

        # Ensure bounds are within the image dimensions
        height, width = image_data.shape
        start_x = max(0, min(start_x, width))
        start_y = max(0, min(start_y, height))
        end_x = max(0, min(end_x, width))
        end_y = max(0, min(end_y, height))

        # Create a mask based on mode
        mask = np.zeros_like(image_data, dtype=np.float32)
        if innerRegion:
            mask[start_y:end_y, start_x:end_x] = 1
        else:  # OutsideRegion
            mask[:, :] = 1
            mask[start_y:end_y, start_x:end_x] = 0

        # Apply the mask to the image data
        cropped_data = image_data * mask
        return cropped_data
