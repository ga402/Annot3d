
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from GraphicsScene import *


class widgetScene(QWidget):
    def __init__(self, layout, parent=None):
        QWidget.__init__(self, parent)
        #self._image = QPixmap
        self.scene = GraphicsScene()
        self.view = QGraphicsView(self.scene)
        #layout = QVBoxLayout()
        layout.addWidget(self.view)
        #self.setLayout(layout)
        self.pixmap_item = QGraphicsPixmapItem()
        #self.pixmap_item.setPixmap(self._image)
        #self.scene.addItem(self.pixmap_item)
        #self.pixmap_item.mousePressEvent = self.pixelSelect
        #self.click_positions = []
    
    def getScene(self):
        return self.scene

    #def mousePressEvent(self, event):
    #    if self.itemAt(event.scenePos(), QTransform()) is None:
    #        self._current_rect_item = QGraphicsRectItem()
    #        self._current_rect_item.setPen(Qt.red)
    #        self._current_rect_item.setFlag(QGraphicsItem.ItemIsMovable, True)
    #        self.addItem(self._current_rect_item)
    #        self._start = event.scenePos()
    #        r = QRectF(self._start, self._start)
    #        self._current_rect_item.setRect(r)
    #    super(GraphicsScene, self).mousePressEvent(event)

    #def mouseMoveEvent(self, event):
    #    if self._current_rect_item is not None:
    #        r = QRectF(self._start, event.scenePos()).normalized()
    #        self._current_rect_item.setRect(r)
    #    super(GraphicsScene, self).mouseMoveEvent(event)

    #def mouseReleaseEvent(self, event):
    #    self._current_rect_item = None
    #    super(GraphicsScene, self).mouseReleaseEvent(event)


    #def pixelSelect(self, event):
    #    self.click_positions.append(event.pos())
    #    if len(self.click_positions) < 4:
    #        return
    #    pen = QPen(Qt.red)
    #    self.scene.addPolygon(QPolygonF(self.click_positions), pen)
    #    for point in self.click_positions:
    #        self.scene.addEllipse(point.x(), point.y(), 2, 2, pen)
    #    self.click_positions = []

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