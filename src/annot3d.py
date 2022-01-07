# Import necessary modules
import sys, os, cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
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
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from libs.imagefuncs import readNdArray
from annot3dGUI import annot3dGUI

style_sheet = """
    QLabel#ImageLabel{
        color: darkgrey;
        border: 2px solid #000000;
        qproperty-alignment: AlignCenter
    }"""


class annot3d(annot3dGUI):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def adjustContrast(self):
        """The slot corresponding to adjusting image contrast."""
        if self.image_label.pixmap() != None:
            self.contrast_adjusted = True

    def adjustBrightness(self):
        """The slot corresponding to adjusting image brightness."""
        if self.image_label.pixmap() != None:
            self.brightness_adjusted = True

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
        #if self.image_smoothing_checked == True:
        #    kernel = np.ones((5, 5), np.float32) / 25
        #    self.cv_image = cv2.filter2D(self.cv_image, -1, kernel)
        #if self.edge_detection_checked == True:
        #    self.cv_image = cv2.Canny(self.cv_image, 100, 200)
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
        #self.filter_2D_cb.setChecked(False)
        #self.canny_cb.setChecked(False)

    def openImageFile(self):
        """Open an image file and display the contents in the label widget."""
        image_file, _ = QFileDialog.getOpenFileName(
            self, "Open Image", os.getenv("HOME"), "Images (*.png *.jpeg *.jpg *.bmp)"
        )
        if image_file:
            self.resetWidgetValues()  # Reset the states of the widgets
            self.apply_process_button.setEnabled(True)
            self.cv_image = cv2.imread(image_file)  # Original image
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
        array_file, _ = QFileDialog.getOpenFileName(
            self, "Open Image", os.getcwd() + "/../images", "nd.array file (*.npy)"
        )
        if array_file:
            self.resetWidgetValues()  # Reset the states of the widgets
            self.apply_process_button.setEnabled(True)
            self.arr = readNdArray(array_file)  # Original image
            self.copy_arr = self.arr.copy()  # A copy of the original image
            # Create a destination image for the contrast and brightness processes
            self.processed_arr = np.zeros(self.arr.shape, dtype=int)
            self.convert2DArrToQImage(
                self.arr[0, 0:512, 0:512, :].squeeze()
            )  # Convert the OpenCV image to a Qt Image
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
        cv_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Get the shape of the image, height * width * channels. BGR/RGB/HSV images have 3 channels
        height, width, channels = cv_image.shape  # Format: (rows, columns, channels)
        # Number of bytes required by the image pixels in a row; dependency on the number of channels
        bytes_per_line = width * channels
        # Create instance of QImage using data from cv_image
        converted_Qt_image = QImage(
            cv_image, width, height, bytes_per_line, QImage.Format_RGB888
        )
        self.image_label.setPixmap(
            QPixmap.fromImage(converted_Qt_image).scaled(
                self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio
            )
        )

    def convert2DArrToQImage(self, image):
        """Load a cv image and convert the image to a Qt QImage. Display the image in image_label."""
        
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
        self.image_label.setPixmap(
            QPixmap.fromImage(converted_Qt_image).scaled(
                self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio
            )
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = annot3d()
    sys.exit(app.exec_())
