
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class drawCanvas(QWidget):
    def __init__(self, layout, parent=None):
        QWidget.__init__(self, parent)
        #self._image = qpixmap
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        #layout = QVBoxLayout()
        #layout.addWidget(self.view)
        self.setLayout(layout)
        self.pixmap_item = QGraphicsPixmapItem()
        #self.pixmap_item.setPixmap(self._image)
        #self.scene.addItem(self.pixmap_item)
        #self.pixmap_item.mousePressEvent = self.pixelSelect
        #self.click_positions = []




#class drawCanvas(QLabel):
#        #Mouse click event
#        def mousePressEvent(self,event):
#            self.flag = True
#            self.x0 = event.x()
#            self.y0 = event.y()
            #Mouse release event
#        def mouseReleaseEvent(self,event):
#            self.flag = False
            #Mouse movement events
#        def mouseMoveEvent(self,event):
#            if self.flag:
#                self.x1 = event.x()
#                self.y1 = event.y()
#                self.update()
                #Draw events
#        def paintEvent(self, event):
#            super().paintEvent(event)
#            rect =QRect(self.x0, self.y0, abs(self.x1-self.#x0), abs(self.y1-self.y0))
#            painter = QPainter(self)
#            painter.setPen(QPen(QColor(255, 255, 0),2,Qt.SolidLine))
#            painter.drawRect(rect)