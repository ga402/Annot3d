# Import necessary modules
import sys, os, cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, QCheckBox, QSpinBox, QDoubleSpinBox, QFrame, QFileDialog, QMessageBox, QHBoxLayout, QVBoxLayout, QAction)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from libs.imagefuncs import readNdArray

style_sheet = """
    QLabel#ImageLabel{
        color: darkgrey;
        border: 2px solid #000000;
        qproperty-alignment: AlignCenter
    }"""
    

class annot3dGUI(QMainWindow):
    """[summary]

    Args:
        QMainWindow ([type]): [description]
    """
    def __init__(self):
        super().__init__()
        self.initializeUI()
    def initializeUI(self):
        """Initialize the window and display its contents to the screen."""
        self.setMinimumSize(900, 600)
        self.setWindowTitle('5.1 - Image Processing GUI')
        self.contrast_adjusted = False
        self.brightness_adjusted = False
        #self.image_smoothing_checked = False
        #self.edge_detection_checked = False
        self.setupWindow()
        self.setupMenu()
        self.show()
    def setupWindow(self):
        """Set up widgets in the main window."""
        # 1. Image label widget
        self.image_label = QLabel()
        self.image_label.setObjectName("ImageLabel")
        # 2. Contrast range widget
        contrast_label = QLabel("Contrast [Range: 0.0:4.0]")
        self.contrast_spinbox = QDoubleSpinBox()
        self.contrast_spinbox.setMinimumWidth(100)
        self.contrast_spinbox.setRange(0.0, 4.0)
        self.contrast_spinbox.setValue(1.0)
        self.contrast_spinbox.setSingleStep(.10)
        self.contrast_spinbox.valueChanged.connect(self.adjustContrast)
        # 3. brightness widget
        brightness_label = QLabel("Brightness [Range: -127:127]")
        self.brightness_spinbox = QSpinBox()
        self.brightness_spinbox.setMinimumWidth(100)
        self.brightness_spinbox.setRange(-127, 127)
        self.brightness_spinbox.setValue(0)
        self.brightness_spinbox.setSingleStep(1)
        self.brightness_spinbox.valueChanged.connect(self.adjustBrightness)
        
        
        # 4. Smoothing widget
        #smoothing_label = QLabel("Image Smoothing Filters")
        #self.filter_2D_cb = QCheckBox("2D Convolution")
        #self.filter_2D_cb.stateChanged.connect(self.imageSmoothingFilter)
        #edges_label = QLabel("Detect Edges")
        #self.canny_cb = QCheckBox("Canny Edge Detector")
        #self.canny_cb.stateChanged.connect(self.edgeDetection)
        
        # apply process button
        self.apply_process_button = QPushButton("Apply Processes")
        self.apply_process_button.setEnabled(False)
        self.apply_process_button.clicked.connect(self.applyImageProcessing)
        reset_button = QPushButton("Reset Image Settings")
        reset_button.clicked.connect(self.resetImageAndSettings)
        
        # Create horizontal and vertical layouts for the side panel and main window
        side_panel_v_box = QVBoxLayout()
        side_panel_v_box.setAlignment(Qt.AlignTop)
        side_panel_v_box.addWidget(contrast_label)
        side_panel_v_box.addWidget(self.contrast_spinbox)
        side_panel_v_box.addWidget(brightness_label)
        side_panel_v_box.addWidget(self.brightness_spinbox)
        side_panel_v_box.addSpacing(15)
        #side_panel_v_box.addWidget(smoothing_label)
        #side_panel_v_box.addWidget(self.filter_2D_cb)
        #side_panel_v_box.addWidget(edges_label)
        #side_panel_v_box.addWidget(self.canny_cb)
        #side_panel_v_box.addWidget(self.apply_process_button)
        side_panel_v_box.addStretch(1)
        side_panel_v_box.addWidget(reset_button)
        side_panel_frame = QFrame()
        side_panel_frame.setMinimumWidth(200)
        side_panel_frame.setFrameStyle(QFrame.WinPanel)
        side_panel_frame.setLayout(side_panel_v_box)
        main_h_box = QHBoxLayout()
        main_h_box.addWidget(self.image_label, 1)
        main_h_box.addWidget(side_panel_frame)
        # Create container widget and set main window's widget
        container = QWidget()
        container.setLayout(main_h_box)
        self.setCentralWidget(container)
        
        
    def setupMenu(self):
        """Simple menu bar to select and save local images ."""
        # Create actions for file menu
        # 1. Open ...
        # 2. Open array ...
        # 3. Save ...
        open_act = QAction('Open...', self)
        open_act.setShortcut('Ctrl+O')
        open_act.triggered.connect(self.openImageFile)
        open_3d_act = QAction('Open 3D array...', self)
        open_3d_act.setShortcut('Ctrl+A')
        open_3d_act.triggered.connect(self.openArrayFile)
        save_act = QAction('Save...', self)
        save_act.setShortcut('Ctrl+S')
        save_act.triggered.connect(self.saveImageFile)
        # Create menu bar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        # Create file menu and add actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(open_act)
        file_menu.addAction(open_3d_act)
        file_menu.addAction(save_act)