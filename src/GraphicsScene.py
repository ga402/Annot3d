from PyQt5 import QtCore, QtGui, QtWidgets
from storeCoords import *

class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(QtCore.QRectF(0, 0, 512, 512),parent)
        self._start = QtCore.QPointF()
        self._current_rect_item = None
        self._coordDict= {}
        self._rectN = None
        self.z = 0
        self._zstart = 0
        self._zend = 0

    def mousePressEvent(self, event):
        if self.itemAt(event.scenePos(), QtGui.QTransform()) is not None:
            self._coords = storeCoords() 
            self._coords.setX(event.scenePos().x())
            self._coords.setY(event.scenePos().y())
            self._coords.setZ0(self.z)
            self._current_rect_item = QtWidgets.QGraphicsRectItem()
            
            self._current_rect_item.setPen(QtCore.Qt.red)
            self._current_rect_item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
            self.addItem(self._current_rect_item)
            self._start = event.scenePos()
            r = QtCore.QRectF(self._start, self._start)
            self._current_rect_item.setRect(r)
        super(GraphicsScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._current_rect_item is not None:
            r = QtCore.QRectF(self._start, event.scenePos()).normalized()
            self._current_rect_item.setRect(r)
        super(GraphicsScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._coords.setW(event.scenePos().x())
        self._coords.setH(event.scenePos().y())
        self._coords.setZ1(self.z)
        self._coordDict[self._rectN] = self._coords.getCoords()
        self._rectN +=1
        self._current_rect_item = None
        print(self._coords)
        super(GraphicsScene, self).mouseReleaseEvent(event)
        
    
    def setRectN(self, rectN):
        self._rectN = rectN
    
    def getRectN(self, rectN):
        return self._rectN
    
    def getPositions(self, event):
        return self._coordDict
    
    def setZ(self, z):
        self.z = z
        
    
        
        
    
