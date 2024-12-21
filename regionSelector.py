from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene, QMessageBox
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtCore import QSizeF
class ResizableRectangle(QGraphicsRectItem):
    linked_rectangles = []  # Shared list of linked rectangles

    def __init__(self, x=0, y=0, width=80, height=80):
        super().__init__(x, y, width, height)
        self.setFlags(QGraphicsRectItem.ItemIsMovable | QGraphicsRectItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setPen(QPen(QColor(128, 0, 128), 2))  # Purple color for rectangle with 2px border
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
        if self._is_in_resize_area(event.pos()):
            self.setCursor(Qt.SizeFDiagCursor)
            self.cursor_in_resize = True
        else:
            self.setCursor(Qt.ArrowCursor)
            self.cursor_in_resize = False

    def mousePressEvent(self, event):
        if self.cursor_in_resize:
            self.resizing = True
            self.start_pos = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
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

            self.sync_with_linked_rectangles()  # Sync changes

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
        self.resizing = False
        super().mouseReleaseEvent(event)

    def _is_in_resize_area(self, pos):
        return abs(pos.x() - self.rect().width()) < self.resize_handle_size and \
               abs(pos.y() - self.rect().height()) < self.resize_handle_size

    def sync_with_linked_rectangles(self):
        valid_rectangles = [rect for rect in self.linked_rectangles if rect.scene() is not None]
        self.linked_rectangles = valid_rectangles  # Remove invalid rectangles

        for rect in valid_rectangles:
            rect.setRect(self.rect())