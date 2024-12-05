from PyQt5 import QtWidgets, uic
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('task4.ui', self)

        # Connect buttons to their methods
        self.switch_button.clicked.connect(self.hide_image_frame_and_label)
        self.pushButton.clicked.connect(self.show_image_frame_and_label)
        self.frame_5.hide()

    def hide_image_frame_and_label(self):
        """Hides imageFrame, frame_3, and label; shows everything else."""
        self.imageFrame.hide()
        self.frame_3.hide()

        # Show all other widgets
        for widget in self.findChildren(QtWidgets.QWidget):
            if widget.objectName() not in ['imageFrame', 'frame_3', 'label']:
                widget.show()

    def show_image_frame_and_label(self):
        """Shows imageFrame, frame_3, and label; hides everything else."""
        self.frame_5.hide()
        self.imageFrame.show()
        self.frame_3.show()

# Entry point of the application
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
