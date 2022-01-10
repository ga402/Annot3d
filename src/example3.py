import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
# importing libraries
from PyQt5.QtWidgets import *

class MainWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)
        self._image = QPixmap("../images/test.png")
        self.pixmap_item = QGraphicsPixmapItem()
        self.pixmap_item.setPixmap(self._image)
        self.scene.addItem(self.pixmap_item)
        self.pixmap_item.mousePressEvent = self.pixelSelect
        self.click_positions = []

    def pixelSelect(self, event):
        self.click_positions.append(event.pos())
        if len(self.click_positions) < 4:
            return
        pen = QPen(Qt.red)
        self.scene.addPolygon(QPolygonF(self.click_positions), pen)
        for point in self.click_positions:
            self.scene.addEllipse(point.x(), point.y(), 2, 2, pen)
        self.click_positions = []


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.resize(640, 480)
    widget.show()
    sys.exit(app.exec_())
