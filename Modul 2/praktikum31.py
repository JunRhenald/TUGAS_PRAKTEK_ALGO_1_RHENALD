import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

class CustomListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item:
            mimeData = QMimeData()
            mimeData.setText(item.text())
            
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            
            if drag.exec_(Qt.MoveAction) == Qt.MoveAction:
                self.takeItem(self.row(item))

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasText():
            self.addItem(event.mimeData().text())
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            super().dropEvent(event)

class DragDropDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop Demo")
        self.setGeometry(300, 300, 600, 400)

        main_layout = QHBoxLayout(self)

        source_layout = QVBoxLayout()
        source_layout.addWidget(QLabel("Source (drag from here):"))
        self.source_list = CustomListWidget()
        self.source_list.addItems(["Apple", "Banana", "Cherry", "Date", "Elderberry"])
        source_layout.addWidget(self.source_list)

        target_layout = QVBoxLayout()
        target_layout.addWidget(QLabel("Target (drop here):"))
        self.target_list = CustomListWidget()
        
        self.clear_btn = QPushButton("Clear Target")
        self.clear_btn.clicked.connect(self.target_list.clear)
        
        target_layout.addWidget(self.target_list)
        target_layout.addWidget(self.clear_btn)

        main_layout.addLayout(source_layout)
        main_layout.addLayout(target_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DragDropDemo()
    window.show()
    sys.exit(app.exec_())