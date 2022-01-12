
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
        self.view.setCursor(Qt.CrossCursor)
        #layout = QVBoxLayout()
        layout.addWidget(self.view)
        #self.setLayout(layout)
        #self.pixmap_item = QGraphicsPixmapItem()
        self._rectN = 0
        self.scene.setRectN(self._rectN)
        #self.pixmap_item.setPixmap(self._image)
        #self.scene.addItem(self.pixmap_item)
        #self.pixmap_item.mousePressEvent = self.pixelSelect
        #self.click_positions = []
    
    def getScene(self):
        return self.scene
    

        
 
        
    
    

