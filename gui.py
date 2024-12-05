# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'task4.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1207, 934)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet("background-color: rgb(233, 233, 241);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setStyleSheet("color: rgb(66, 31, 99);\n"
"font: 9pt \"Microsoft Sans Serif\";")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.output1 = QtWidgets.QRadioButton(self.frame_3)
        self.output1.setStyleSheet("color: rgb(66, 31, 99);\n"
"font: 9pt \"Microsoft Sans Serif\";")
        self.output1.setChecked(True)
        self.output1.setObjectName("output1")
        self.output_buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.output_buttonGroup.setObjectName("output_buttonGroup")
        self.output_buttonGroup.addButton(self.output1)
        self.gridLayout_3.addWidget(self.output1, 15, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(66, 31, 99);")
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 12, 0, 1, 1)
        self.output2 = QtWidgets.QRadioButton(self.frame_3)
        self.output2.setObjectName("output2")
        self.output_buttonGroup.addButton(self.output2)
        self.gridLayout_3.addWidget(self.output2, 15, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(66, 31, 99);\n"
"font: 11pt \"Microsoft Sans Serif\";")
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 7, 0, 1, 1)
        self.output_mixer1 = QtWidgets.QGraphicsView(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output_mixer1.sizePolicy().hasHeightForWidth())
        self.output_mixer1.setSizePolicy(sizePolicy)
        self.output_mixer1.setStyleSheet("border-radius: 25px;\n"
"buttoon-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"widget-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.output_mixer1.setObjectName("output_mixer1")
        self.gridLayout_3.addWidget(self.output_mixer1, 0, 2, 15, 1)
        self.out_region_radioButton = QtWidgets.QRadioButton(self.frame_3)
        self.out_region_radioButton.setStyleSheet("color: rgb(66, 31, 99);\n"
"font: 9pt \"Microsoft Sans Serif\";")
        self.out_region_radioButton.setCheckable(True)
        self.out_region_radioButton.setChecked(True)
        self.out_region_radioButton.setObjectName("out_region_radioButton")
        self.region_buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.region_buttonGroup.setObjectName("region_buttonGroup")
        self.region_buttonGroup.addButton(self.out_region_radioButton)
        self.gridLayout_3.addWidget(self.out_region_radioButton, 2, 1, 1, 1)
        self.output_mixer2 = QtWidgets.QGraphicsView(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output_mixer2.sizePolicy().hasHeightForWidth())
        self.output_mixer2.setSizePolicy(sizePolicy)
        self.output_mixer2.setStyleSheet("border-radius: 25px;\n"
"buttoon-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"widget-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.output_mixer2.setObjectName("output_mixer2")
        self.gridLayout_3.addWidget(self.output_mixer2, 0, 3, 15, 1)
        self.real_imaginary = QtWidgets.QRadioButton(self.frame_3)
        self.real_imaginary.setStyleSheet("color: rgb(66, 31, 99);\n"
"font: 9pt \"Microsoft Sans Serif\";")
        self.real_imaginary.setChecked(True)
        self.real_imaginary.setObjectName("real_imaginary")
        self.components_buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.components_buttonGroup.setObjectName("components_buttonGroup")
        self.components_buttonGroup.addButton(self.real_imaginary)
        self.gridLayout_3.addWidget(self.real_imaginary, 9, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(66, 31, 99);\n"
"font: 11pt \"Microsoft Sans Serif\";")
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem1, 6, 0, 1, 1)
        self.region_selecter = QtWidgets.QSlider(self.frame_3)
        self.region_selecter.setStyleSheet("/* 441F62\n"
"CE9BFA\n"
"D9B1FA\n"
"B6DDFE*/\n"
"QSlider::groove:horizontal {\n"
"    height: 8px;\n"
"    background: #B5A5F9; /* Updated lighter color */\n"
"    border-radius: 4px;\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background: #9385E5; /* Updated darker color */\n"
"    border: 2px solid #B5A5F9; /* Updated lighter color */\n"
"    width: 20px;\n"
"    height: 20px;\n"
"    margin: -6px 0;\n"
"    border-radius: 10px;\n"
"}\n"
"QSlider::sub-page:horizontal {\n"
"    background: #9385E5; /* Updated darker color */\n"
"    border-radius: 4px;\n"
"}\n"
"QSlider::add-page:horizontal {\n"
"    background: #B5A5F9; /* Updated lighter color */\n"
"    border-radius: 4px;\n"
"}\n"
"")
        self.region_selecter.setOrientation(QtCore.Qt.Horizontal)
        self.region_selecter.setObjectName("region_selecter")
        self.gridLayout_3.addWidget(self.region_selecter, 4, 0, 1, 2)
        self.in_region_radioButton = QtWidgets.QRadioButton(self.frame_3)
        self.in_region_radioButton.setStyleSheet("color: rgb(66, 31, 99);\n"
"font: 9pt \"Microsoft Sans Serif\";")
        self.in_region_radioButton.setChecked(False)
        self.in_region_radioButton.setObjectName("in_region_radioButton")
        self.region_buttonGroup.addButton(self.in_region_radioButton)
        self.gridLayout_3.addWidget(self.in_region_radioButton, 2, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 12, 1, 1, 1)
        self.magnitude_phase = QtWidgets.QRadioButton(self.frame_3)
        self.magnitude_phase.setStyleSheet("color: rgb(66, 31, 99);\n"
"font: 9pt \"Microsoft Sans Serif\";")
        self.magnitude_phase.setObjectName("magnitude_phase")
        self.components_buttonGroup.addButton(self.magnitude_phase)
        self.gridLayout_3.addWidget(self.magnitude_phase, 9, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame_3, 4, 0, 1, 1)
        self.imageFrame = QtWidgets.QFrame(self.centralwidget)
        self.imageFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.imageFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.imageFrame.setObjectName("imageFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.imageFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.Fourier_comboBox_3 = QtWidgets.QComboBox(self.imageFrame)
        self.Fourier_comboBox_3.setStyleSheet("QComboBox {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: #9688E9;  /* Background color */\n"
"    border: 1px solid #1C1C1C;\n"
"    border-radius: 15px;  /* Rounded corners */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"}\n"
"QComboBox::drop-down {\n"
"   \n"
"    color: #ffffff;\n"
"    border-radius: 10px;  /* Rounded corners for the arrow box */\n"
"    background-color: #9688E9;\n"
"    width: 30px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    color: white;  /* Arrow color */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #1C1C1C;\n"
"    selection-background-color: #9688E9;  /* Selected item background color */\n"
"    background-color: #9688E9;  /* Dropdown background color */\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"}")
        self.Fourier_comboBox_3.setObjectName("Fourier_comboBox_3")
        self.Fourier_comboBox_3.addItem("")
        self.Fourier_comboBox_3.addItem("")
        self.Fourier_comboBox_3.addItem("")
        self.Fourier_comboBox_3.addItem("")
        self.gridLayout.addWidget(self.Fourier_comboBox_3, 16, 4, 1, 1)
        self.Glabel1 = QtWidgets.QLabel(self.imageFrame)
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Glabel1.setFont(font)
        self.Glabel1.setStyleSheet("color: rgb(66, 31, 99);\n"
"font: 11pt \"Microsoft Sans Serif\";")
        self.Glabel1.setObjectName("Glabel1")
        self.gridLayout.addWidget(self.Glabel1, 10, 0, 1, 1)
        self.Gimage3 = QtWidgets.QGraphicsView(self.imageFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Gimage3.sizePolicy().hasHeightForWidth())
        self.Gimage3.setSizePolicy(sizePolicy)
        self.Gimage3.setStyleSheet("border-radius: 25px;\n"
"buttoon-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"widget-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.Gimage3.setObjectName("Gimage3")
        self.gridLayout.addWidget(self.Gimage3, 13, 4, 1, 1)
        self.Gimage4 = QtWidgets.QGraphicsView(self.imageFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Gimage4.sizePolicy().hasHeightForWidth())
        self.Gimage4.setSizePolicy(sizePolicy)
        self.Gimage4.setStyleSheet("border-radius: 25px;\n"
"buttoon-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"widget-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.Gimage4.setObjectName("Gimage4")
        self.gridLayout.addWidget(self.Gimage4, 13, 6, 1, 1)
        self.image1 = QtWidgets.QGraphicsView(self.imageFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image1.sizePolicy().hasHeightForWidth())
        self.image1.setSizePolicy(sizePolicy)
        self.image1.setStyleSheet("border-radius: 25px;\n"
"buttoon-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"widget-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.image1.setObjectName("image1")
        self.gridLayout.addWidget(self.image1, 9, 0, 1, 1)
        self.image4 = QtWidgets.QGraphicsView(self.imageFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image4.sizePolicy().hasHeightForWidth())
        self.image4.setSizePolicy(sizePolicy)
        self.image4.setStyleSheet("border-radius: 25px;\n"
"buttoon-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"widget-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.image4.setObjectName("image4")
        self.gridLayout.addWidget(self.image4, 9, 6, 1, 1)
        self.Gimage2 = QtWidgets.QGraphicsView(self.imageFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Gimage2.sizePolicy().hasHeightForWidth())
        self.Gimage2.setSizePolicy(sizePolicy)
        self.Gimage2.setStyleSheet("border-radius: 25px;\n"
"buttoon-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"widget-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.Gimage2.setObjectName("Gimage2")
        self.gridLayout.addWidget(self.Gimage2, 13, 2, 1, 1)
        self.Fourier_comboBox_2 = QtWidgets.QComboBox(self.imageFrame)
        self.Fourier_comboBox_2.setStyleSheet("QComboBox {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: #9688E9;  /* Background color */\n"
"    border: 1px solid #1C1C1C;\n"
"    border-radius: 15px;  /* Rounded corners */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"}\n"
"QComboBox::drop-down {\n"
"   \n"
"    color: #ffffff;\n"
"    border-radius: 10px;  /* Rounded corners for the arrow box */\n"
"    background-color: #9688E9;\n"
"    width: 30px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    color: white;  /* Arrow color */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #1C1C1C;\n"
"    selection-background-color: #9688E9;  /* Selected item background color */\n"
"    background-color: #9688E9;  /* Dropdown background color */\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"}")
        self.Fourier_comboBox_2.setObjectName("Fourier_comboBox_2")
        self.Fourier_comboBox_2.addItem("")
        self.Fourier_comboBox_2.addItem("")
        self.Fourier_comboBox_2.addItem("")
        self.Fourier_comboBox_2.addItem("")
        self.gridLayout.addWidget(self.Fourier_comboBox_2, 16, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.imageFrame)
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(66, 31, 99);\n"
"font: 11pt \"Microsoft Sans Serif\";")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 8, 0, 1, 1)
        self.Gimage1 = QtWidgets.QGraphicsView(self.imageFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Gimage1.sizePolicy().hasHeightForWidth())
        self.Gimage1.setSizePolicy(sizePolicy)
        self.Gimage1.setMouseTracking(True)
        self.Gimage1.setAutoFillBackground(False)
        self.Gimage1.setStyleSheet("border-radius: 25px;\n"
"buttoon-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"widget-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.Gimage1.setObjectName("Gimage1")
        self.gridLayout.addWidget(self.Gimage1, 13, 0, 1, 1)
        self.weight_1 = QtWidgets.QSlider(self.imageFrame)
        self.weight_1.setStyleSheet("\n"
"QSlider::groove:vertical {\n"
"    width: 8px;\n"
"    background: #B5A5F9;\n"
"    border-radius: 4px;\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background: #9385E5;\n"
"    border: 2px solid #B5A5F9;\n"
"    width: 20px;\n"
"    height: 20px;\n"
"    margin: 0 -6px;\n"
"    border-radius: 10px;\n"
"}\n"
"QSlider::sub-page:vertical {\n"
"    background: #9385E5;\n"
"    border-radius: 4px;\n"
"}\n"
"QSlider::add-page:vertical {\n"
"    background: #B5A5F9;\n"
"    border-radius: 4px;\n"
"}\n"
"")
        self.weight_1.setOrientation(QtCore.Qt.Vertical)
        self.weight_1.setObjectName("weight_1")
        self.gridLayout.addWidget(self.weight_1, 13, 1, 1, 1)
        self.Fourier_comboBox_1 = QtWidgets.QComboBox(self.imageFrame)
        self.Fourier_comboBox_1.setStyleSheet("QComboBox {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: #9688E9;  /* Background color */\n"
"    border: 1px solid #1C1C1C;\n"
"    border-radius: 15px;  /* Rounded corners */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"}\n"
"QComboBox::drop-down {\n"
"   \n"
"    color: #ffffff;\n"
"    border-radius: 10px;  /* Rounded corners for the arrow box */\n"
"    background-color: #9688E9;\n"
"    width: 30px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    color: white;  /* Arrow color */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #1C1C1C;\n"
"    selection-background-color: #9688E9;  /* Selected item background color */\n"
"    background-color: #9688E9;  /* Dropdown background color */\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"}")
        self.Fourier_comboBox_1.setObjectName("Fourier_comboBox_1")
        self.Fourier_comboBox_1.addItem("")
        self.Fourier_comboBox_1.addItem("")
        self.Fourier_comboBox_1.addItem("")
        self.Fourier_comboBox_1.addItem("")
        self.gridLayout.addWidget(self.Fourier_comboBox_1, 16, 0, 1, 1)
        self.image3 = QtWidgets.QGraphicsView(self.imageFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image3.sizePolicy().hasHeightForWidth())
        self.image3.setSizePolicy(sizePolicy)
        self.image3.setStyleSheet("border-radius: 25px;\n"
"buttoon-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"widget-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.image3.setObjectName("image3")
        self.gridLayout.addWidget(self.image3, 9, 4, 1, 1)
        self.weight_4 = QtWidgets.QSlider(self.imageFrame)
        self.weight_4.setStyleSheet("\n"
"QSlider::groove:vertical {\n"
"    width: 8px;\n"
"    background: #B5A5F9;\n"
"    border-radius: 4px;\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background: #9385E5;\n"
"    border: 2px solid #B5A5F9;\n"
"    width: 20px;\n"
"    height: 20px;\n"
"    margin: 0 -6px;\n"
"    border-radius: 10px;\n"
"}\n"
"QSlider::sub-page:vertical {\n"
"    background: #9385E5;\n"
"    border-radius: 4px;\n"
"}\n"
"QSlider::add-page:vertical {\n"
"    background: #B5A5F9;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"")
        self.weight_4.setOrientation(QtCore.Qt.Vertical)
        self.weight_4.setObjectName("weight_4")
        self.gridLayout.addWidget(self.weight_4, 13, 7, 1, 1)
        self.image2 = QtWidgets.QGraphicsView(self.imageFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image2.sizePolicy().hasHeightForWidth())
        self.image2.setSizePolicy(sizePolicy)
        self.image2.setStyleSheet("border-radius: 25px;\n"
"buttoon-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"widget-shadow: 2px 2px 5px rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.image2.setObjectName("image2")
        self.gridLayout.addWidget(self.image2, 9, 2, 1, 1)
        self.Fourier_comboBox_4 = QtWidgets.QComboBox(self.imageFrame)
        self.Fourier_comboBox_4.setStyleSheet("QComboBox {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: #9688E9;  /* Background color */\n"
"    border: 1px solid #1C1C1C;\n"
"    border-radius: 15px;  /* Rounded corners */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"}\n"
"QComboBox::drop-down {\n"
"   \n"
"    color: #ffffff;\n"
"    border-radius: 10px;  /* Rounded corners for the arrow box */\n"
"    background-color: #9688E9;\n"
"    width: 30px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    color: white;  /* Arrow color */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #1C1C1C;\n"
"    selection-background-color: #9688E9;  /* Selected item background color */\n"
"    background-color: #9688E9;  /* Dropdown background color */\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"}")
        self.Fourier_comboBox_4.setObjectName("Fourier_comboBox_4")
        self.Fourier_comboBox_4.addItem("")
        self.Fourier_comboBox_4.addItem("")
        self.Fourier_comboBox_4.addItem("")
        self.Fourier_comboBox_4.addItem("")
        self.gridLayout.addWidget(self.Fourier_comboBox_4, 16, 6, 1, 1)
        self.weight_2 = QtWidgets.QSlider(self.imageFrame)
        self.weight_2.setStyleSheet("\n"
"QSlider::groove:vertical {\n"
"    width: 8px;\n"
"    background: #B5A5F9;\n"
"    border-radius: 4px;\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background: #9385E5;\n"
"    border: 2px solid #B5A5F9;\n"
"    width: 20px;\n"
"    height: 20px;\n"
"    margin: 0 -6px;\n"
"    border-radius: 10px;\n"
"}\n"
"QSlider::sub-page:vertical {\n"
"    background: #9385E5;\n"
"    border-radius: 4px;\n"
"}\n"
"QSlider::add-page:vertical {\n"
"    background: #B5A5F9;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"")
        self.weight_2.setOrientation(QtCore.Qt.Vertical)
        self.weight_2.setObjectName("weight_2")
        self.gridLayout.addWidget(self.weight_2, 13, 3, 1, 1)
        self.weight_3 = QtWidgets.QSlider(self.imageFrame)
        self.weight_3.setStyleSheet("\n"
"QSlider::groove:vertical {\n"
"    width: 8px;\n"
"    background: #B5A5F9;\n"
"    border-radius: 4px;\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background: #9385E5;\n"
"    border: 2px solid #B5A5F9;\n"
"    width: 20px;\n"
"    height: 20px;\n"
"    margin: 0 -6px;\n"
"    border-radius: 10px;\n"
"}\n"
"QSlider::sub-page:vertical {\n"
"    background: #9385E5;\n"
"    border-radius: 4px;\n"
"}\n"
"QSlider::add-page:vertical {\n"
"    background: #B5A5F9;\n"
"    border-radius: 4px;\n"
"}\n"
"")
        self.weight_3.setOrientation(QtCore.Qt.Vertical)
        self.weight_3.setObjectName("weight_3")
        self.gridLayout.addWidget(self.weight_3, 13, 5, 1, 1)
        self.gridLayout_2.addWidget(self.imageFrame, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(66, 31, 99);")
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1207, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.output1.setText(_translate("MainWindow", "Output Channel 1"))
        self.label_3.setText(_translate("MainWindow", "Mixer:"))
        self.output2.setText(_translate("MainWindow", "Output Channel 2"))
        self.label_6.setText(_translate("MainWindow", "Choose Components:"))
        self.out_region_radioButton.setText(_translate("MainWindow", "Outer Region"))
        self.real_imaginary.setText(_translate("MainWindow", "Real/Imaginary"))
        self.label_5.setText(_translate("MainWindow", "Select Region:"))
        self.in_region_radioButton.setText(_translate("MainWindow", "Inner Region"))
        self.magnitude_phase.setText(_translate("MainWindow", "Magnitude/Phase"))
        self.Fourier_comboBox_3.setItemText(0, _translate("MainWindow", "FT Real"))
        self.Fourier_comboBox_3.setItemText(1, _translate("MainWindow", "FT Imaginary"))
        self.Fourier_comboBox_3.setItemText(2, _translate("MainWindow", "FT Magnitude"))
        self.Fourier_comboBox_3.setItemText(3, _translate("MainWindow", "FT Phase"))
        self.Glabel1.setText(_translate("MainWindow", "Fourier Transform"))
        self.Fourier_comboBox_2.setItemText(0, _translate("MainWindow", "FT Real"))
        self.Fourier_comboBox_2.setItemText(1, _translate("MainWindow", "FT Imaginary"))
        self.Fourier_comboBox_2.setItemText(2, _translate("MainWindow", "FT Magnitude"))
        self.Fourier_comboBox_2.setItemText(3, _translate("MainWindow", "FT Phase"))
        self.label_2.setText(_translate("MainWindow", "Input Table"))
        self.Fourier_comboBox_1.setItemText(0, _translate("MainWindow", "FT Real"))
        self.Fourier_comboBox_1.setItemText(1, _translate("MainWindow", "FT Imaginary"))
        self.Fourier_comboBox_1.setItemText(2, _translate("MainWindow", "FT Magnitude"))
        self.Fourier_comboBox_1.setItemText(3, _translate("MainWindow", "FT Phase"))
        self.Fourier_comboBox_4.setItemText(0, _translate("MainWindow", "FT Real"))
        self.Fourier_comboBox_4.setItemText(1, _translate("MainWindow", "FT Imaginary"))
        self.Fourier_comboBox_4.setItemText(2, _translate("MainWindow", "FT Magnitude"))
        self.Fourier_comboBox_4.setItemText(3, _translate("MainWindow", "FT Phase"))
        self.label.setText(_translate("MainWindow", "FourierBlend Studio"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
