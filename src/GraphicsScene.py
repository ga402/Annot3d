from PyQt5 import QtCore, QtGui, QtWidgets

class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(QtCore.QRectF(0, 0, 512, 512),parent)
        self._start = QtCore.QPointF()
        self._current_rect_item = None

    def mousePressEvent(self, event):
        if self.itemAt(event.scenePos(), QtGui.QTransform()) is None:
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
        self._current_rect_item = None
        super(GraphicsScene, self).mouseReleaseEvent(event)