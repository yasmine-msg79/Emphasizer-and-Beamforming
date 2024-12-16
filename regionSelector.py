from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene, QMessageBox
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtCore import QSizeF
class ResizableRectangle(QGraphicsRectItem):
    def __init__(self, x=0, y=0, width=80, height=80):
        super().__init__(x, y, width, height)
        self.setFlags(QGraphicsRectItem.ItemIsMovable | QGraphicsRectItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setPen(QPen(QColor(128, 0, 128), 2))  # Purple color for rectangle with 2px border
        self.resize_handle_size = 10
        self.resizing = False
        self.cursor_in_resize = False

    def hoverMoveEvent(self, event):
        # Change the cursor when hovering over the corners
        if self._is_in_resize_area(event.pos()):
            self.setCursor(Qt.SizeFDiagCursor)
            self.cursor_in_resize = True
        else:
            self.setCursor(Qt.ArrowCursor)
            self.cursor_in_resize = False

    def mousePressEvent(self, event):
        # Start resizing if clicked near the corner
        if self.cursor_in_resize:
            self.resizing = True
            self.start_pos = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.resizing:
            # Calculate the delta for width and height
            delta = event.pos() - self.start_pos
            delta_width = delta.x()
            delta_height = delta.y()

            # Ensure the new size respects minimum resize handle size
            new_width = max(self.rect().width() + delta_width, self.resize_handle_size)
            new_height = max(self.rect().height() + delta_height, self.resize_handle_size)

            # Update the rectangle size
            new_rect = QRectF(self.rect().topLeft(), QSizeF(new_width, new_height))
            self.setRect(new_rect)

            # Update the starting position for the next movement
            self.start_pos = event.pos()
        else:
            super().mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        self.resizing = False
        super().mouseReleaseEvent(event)

    def _is_in_resize_area(self, pos):
        # Check if the cursor is in the bottom-right corner
        return abs(pos.x() - self.rect().width()) < self.resize_handle_size and \
               abs(pos.y() - self.rect().height()) < self.resize_handle_size

