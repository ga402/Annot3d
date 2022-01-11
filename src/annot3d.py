# Import necessary modules
from abc import abstractmethod
import sys, os, cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsPixmapItem,
    QLabel,
    QMainWindow,
    QWidget,
    QPushButton,
    QCheckBox,
    QSpinBox,
    QDoubleSpinBox,
    QFrame,
    QFileDialog,
    QMessageBox,
    QHBoxLayout,
    QVBoxLayout,
    QAction,
)
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import Qt
#from drawCanvas import drawRectangle
from libs.imagefuncs import readNdArray
from annot3dGUI import annot3dGUI
from typing import Final
#from drawCanvas import *

#from libs.shape import Shape
#from libs.measure import distance

CURSOR_DEFAULT = Qt.ArrowCursor
CURSOR_POINT = Qt.PointingHandCursor
CURSOR_DRAW = Qt.CrossCursor
CURSOR_MOVE = Qt.ClosedHandCursor
CURSOR_GRAB = Qt.OpenHandCursor



style_sheet = """
    QLabel#ImageLabel{
        color: darkgrey;
        border: 2px solid #000000;
        qproperty-alignment: AlignCenter
    }"""


class annot3d(annot3dGUI, QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()
        self._cursor = CURSOR_DEFAULT
        self.drawing_line_color = QColor(255, 255, 0)
        self.drawing_rect_color = QColor(255, 255, 0)
        self.z = 0
        self.y = 0
        self.x = 0
        self.xy_adjust = 10
        self.y_length: Final = 512
        self.x_length: Final = 512
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.flag = False
        self.pixmap_item = QGraphicsPixmapItem()

    def adjustContrast(self):
        """The slot corresponding to adjusting image contrast."""
        if self.image_label.pixmap() != None:
            self.contrast_adjusted = True

    def adjustBrightness(self):
        """The slot corresponding to adjusting image brightness."""
        if self.image_label.pixmap() != None:
            self.brightness_adjusted = True
     
    
    def pushDownButton(self):
        if (self.z -1) < 0:
            self.z = self.z
        else:
            self.z = self.z -1
            
        img = self.subsetImage(self.arr, self.z, self.x, self.y)
        self.convert2DArrToQImage(img)  

    def pushUpButton(self):
        if (self.z + 1) >= self.z_max-1:
            self.z = self.z_max -1
        else:
            self.z = self.z + 1
            
        img = self.subsetImage(self.arr, self.z, self.x, self.y)
        self.convert2DArrToQImage(img)  

    def joystick_up(self):
        if (self.y + self.xy_adjust) >= self.y_max-1:
            self.y = self.y_max -1
        else:
            self.y = self.y +self.xy_adjust
        img = self.subsetImage(self.arr, self.z, self.x, self.y)
        self.convert2DArrToQImage(img)  
    
    def joystick_down(self):
        if (self.y - self.xy_adjust) <0:
            self.y = 0
        else:
            self.y = self.y -self.xy_adjust
        img = self.subsetImage(self.arr, self.z, self.x, self.y)
        self.convert2DArrToQImage(img)  

    def joystick_left(self):
        if (self.x - self.xy_adjust) <0:
            self.x = 0
        else:
            self.x = self.x -self.xy_adjust
        img = self.subsetImage(self.arr, self.z, self.x, self.y)
        self.convert2DArrToQImage(img)  

    def joystick_right(self):
        if (self.x + 1) >= self.x_max-1:
            self.x = self.x_max -1
        else:
            self.x = self.x +self.xy_adjust
        img = self.subsetImage(self.arr, self.z, self.x, self.y)
        self.convert2DArrToQImage(img)  
    
    # mouse events
    #def mousePressEvent(self,event):
    #    self.flag = True
    #    self.x0 = event.x()
    #    self.y0 = event.y()
        #Mouse release event
    #def mouseReleaseEvent(self,event):
    #    self.flag = False
        #Mouse movement events
    #def mouseMoveEvent(self,event):
    #    if self.flag:
    #        self.x1 = event.x()
    #        self.y1 = event.y()
    #        self.image_label.update()

            #Draw events
    #def paintEvent(self, event): 
    #    if self.flag and self.image_file:
    #        super().paintEvent(event)
    #        rect =QRect(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))
    #        painter = QPainter(self)
    #        painter.drawPixmap(self.rect(), self.image_label.pixmap())
            #painter.setRenderHint(QPainter.Antialiasing, True)
    #        painter.setPen(QPen(QColor(255, 255, 0),2,Qt.SolidLine))
    #        painter.drawRect(rect)
    
            #self.image_label.update()

    #def imageSmoothingFilter(self, state):
    #    """The slot corresponding to applying 2D Convolution for smoothing the image."""
    #    if state == Qt.Checked and self.image_label.pixmap() != None:
    #        self.image_smoothing_checked = True
    #    elif state != Qt.Checked and self.image_label.pixmap() != None:
    #        self.image_smoothing_checked = False

    #def edgeDetection(self, state):
    #    """The slot corresponding to applying edge detection."""
    #    if state == Qt.Checked and self.image_label.pixmap() != None:
    #        self.edge_detection_checked = True
    #    elif state != Qt.Checked and self.image_label.pixmap() != None:
    #        self.edge_detection_checked = False

    def applyImageProcessing(self):
        """For the boolean variables related to the image processing techniques, if True, apply the corresponding process to the image and display the changes in the QLabel, image_label."""
        if self.contrast_adjusted == True or self.brightness_adjusted == True:
            contrast = self.contrast_spinbox.value()
            brightness = self.brightness_spinbox.value()
            
            self.cv_image = cv2.convertScaleAbs(
                self.cv_image, self.processed_cv_image, contrast, brightness
            )
        self.convertCVToQImage(self.cv_image)
        self.image_label.repaint()  # Repaint the updated image on the label

    def resetImageAndSettings(self):
        """Reset the displayed image and widgets used for image processing."""
        answer = QMessageBox.information(
            self,
            "Reset Image",
            "Are you sure you want to reset the image settings?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer == QMessageBox.No:
            pass
        elif answer == QMessageBox.Yes and self.image_label.pixmap() != None:
            self.resetWidgetValues()
            self.cv_image = self.copy_cv_image
            self.convertCVToQImage(self.copy_cv_image)

    def resetWidgetValues(self):
        """Reset the spinbox and checkbox values to their beginning values."""
        self.contrast_spinbox.setValue(1.0)
        self.brightness_spinbox.setValue(0)


    def openImageFile(self):
        """Open an image file and display the contents in the label widget."""
        self.image_file, _ = QFileDialog.getOpenFileName(
            self, "Open Image", os.getcwd() + "/../images", "Images (*.png *.jpeg *.jpg *.bmp)"
        )
        if self.image_file:
            self.resetWidgetValues()  # Reset the states of the widgets
            self.apply_process_button.setEnabled(True)
            self.cv_image = cv2.imread(self.image_file)  # Original image
            self.copy_cv_image = self.cv_image  # A copy of the original image
            # Create a destination image for the contrast and brightness processes
            self.processed_cv_image = np.zeros(self.cv_image.shape, self.cv_image.dtype)
            self.convertCVToQImage(
                self.cv_image
            )  # Convert the OpenCV image to a Qt Image
        else:
            QMessageBox.information(
                self, "Error", "No image was loaded.", QMessageBox.Ok
            )

    def openArrayFile(self):
        """Open an image file and display the contents in the label widget."""
        self.image_file, _ = QFileDialog.getOpenFileName(
            self, "Open Image", os.getcwd() + "/../images", "nd.array file (*.npy)"
        )
        if self.image_file:
            self.resetWidgetValues()  # Reset the states of the widgets
            self.apply_process_button.setEnabled(True)
            self.arr = readNdArray(self.image_file)  # Original image
            self.z_max, self.y_max, self.x_max, _ = self.arr.shape
            self.copy_arr = self.arr.copy()  # A copy of the original image
            # Create a destination image for the contrast and brightness processes
            self.processed_arr = np.zeros(self.arr.shape, dtype=int)
        
            img = self.subsetImage(self.arr, self.z, self.x, self.y)
            self.convert2DArrToQImage(img)  # Convert the OpenCV image to a Qt Image
        else:
            QMessageBox.information(
                self, "Error", "No image was loaded.", QMessageBox.Ok
            )

    def saveImageFile(self):
        """Save the contents of the image_label to file."""
        image_file, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            os.getenv("HOME"),
            "JPEG (*.jpeg);;JPG (*.jpg);;PNG (*.png);;Bitmap (*.bmp)",
        )
        if image_file and self.image_label.pixmap() != None:
            # Save the file using OpenCV's imwrite() function
            cv2.imwrite(image_file, self.cv_image)
        else:
            QMessageBox.information(
                self, "Error", "Unable to save image.", QMessageBox.Ok
            )

    def convertCVToQImage(self, image):
        """Load a cv image and convert the image to a Qt QImage. Display the image in image_label."""
        #self.image_label = drawCanvas(self)
        cv_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Get the shape of the image, height * width * channels. BGR/RGB/HSV images have 3 channels
        height, width, channels = cv_image.shape  # Format: (rows, columns, channels)
        # Number of bytes required by the image pixels in a row; dependency on the number of channels
        bytes_per_line = width * channels
        # Create instance of QImage using data from cv_image
        converted_Qt_image = QImage(
            cv_image, width, height, bytes_per_line, QImage.Format_RGB888
        )
        self.pixmap_item.setPixmap(
            QPixmap.fromImage(converted_Qt_image).scaled(
                self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio
            )
        )
        self.scene.addItem(self.pixmap_item)
        self.image_label.setCursor(Qt.CrossCursor)
        #self.image_label.setCursor(Qt.CrossCursor)
        #self.show()



    def subsetImage(self, image, z, x, y):
        
        if z >= self.z_max and z >= 0:
            z = self.z_max
        elif z <0:
            z = 0
                        
        if ((x + self.x_length) >= self.x_max) and x >=0:
            x1 = self.x_max
            x0 = self.x_max - self.x_length
        elif x <0:
            x0 = 0
            x1 = self.x_length 
        else:
            x0 = x
            x1 = x + self.x_length
        
        if (y + self.x_length) >= self.y_max:
            y1 = self.y_max
            y0 = self.y_max - self.y_length
        elif x <0:
            y0 = 0
            y1 = self.y_length 
        else:
            y0 = y
            y1 = y + self.y_length
              
        return image[z, x0:x1, y0:y1, :].squeeze()*4



    def convert2DArrToQImage(self, image):
        """Load a cv image and convert the image to a Qt QImage. Display the image in image_label."""
        
        #self.image_label = drawCanvas(self)
        # transposition required to fit the Qimage format requires a C-order format
        image = np.transpose(image,(1,0,2)).copy()
        # Get the shape of the image, height * width * channels. BGR/RGB/HSV images have 3 channels
        height, width, channels = image.shape  # Format: (rows, columns, channels)
        # Number of bytes required by the image pixels in a row; dependency on the number of channels
        bytes_per_line = width * channels
        # Create instance of QImage using data from cv_image
        converted_Qt_image = QImage(
            image, width, height, bytes_per_line, QImage.Format_RGB888
        )
        self.pixmap_item.setPixmap(
            QPixmap.fromImage(converted_Qt_image).scaled(
                self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio
            )
        )
        self.image_label.setCursor(Qt.CrossCursor)
        
        self.scene.addItem(self.pixmap_item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = annot3d()
    sys.exit(app.exec_())
