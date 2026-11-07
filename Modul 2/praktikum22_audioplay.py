
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

class SimpleMediaPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Media Player")
        self.setGeometry(300, 300, 500, 200)

        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Control buttons
        btn_layout = QHBoxLayout()
        self.play_btn = QPushButton("▶ Play")
        self.pause_btn = QPushButton("⏸ Pause")
        self.stop_btn = QPushButton("⏹ Stop")
        self.add_btn = QPushButton("+ Add File")

        btn_layout.addWidget(self.play_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.add_btn)

        # Progress slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.set_position)

        # Label
        self.current_label = QLabel("No file playing")
        layout.addLayout(btn_layout)
        layout.addWidget(self.slider)
        layout.addWidget(self.current_label)

        # Signal connections
        self.play_btn.clicked.connect(self.player.play)
        self.pause_btn.clicked.connect(self.player.pause)
        self.stop_btn.clicked.connect(self.player.stop)
        self.add_btn.clicked.connect(self.add_file)

        self.player.positionChanged.connect(self.update_slider)
        self.player.durationChanged.connect(self.set_duration)
        self.player.currentMediaChanged.connect(self.update_label)

    def add_file(self):
          files, _ = QFileDialog.getOpenFileNames(self,"Select Audio Files", "", "Audio Files (*.mp3 *.wav)")
          for file in files:
               self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(file)))
               self.current_label.setText(f"Added: {file.split('/')[-1]}")

    def set_position(self, position):
         self.player.setPosition(position)

    def update_slider(self, position):
         self.slider.setValue(position)

    def set_duration(self, duration):
         self.slider.setRange(0, duration)

    def update_label(self, media):
         if media.isNull():
              self.current_label.setText("No file playing")
         else:
              self.current_label.setText(f"Playing: {media.canonicalUrl().fileName()}")

if __name__ =="__main__":
    app = QApplication(sys.argv)
    window = SimpleMediaPlayer()
    window.show()
    sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

class SimpleMediaPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Media Player")
        self.setGeometry(300, 300, 500, 200)

        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Control buttons
        btn_layout = QHBoxLayout()
        self.play_btn = QPushButton("▶ Play")
        self.pause_btn = QPushButton("⏸ Pause")
        self.stop_btn = QPushButton("⏹ Stop")
        self.add_btn = QPushButton("+ Add File")

        btn_layout.addWidget(self.play_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.add_btn)

        # Progress slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.set_position)

        # Label
        self.current_label = QLabel("No file playing")
        layout.addLayout(btn_layout)
        layout.addWidget(self.slider)
        layout.addWidget(self.current_label)

        # Signal connections
        self.play_btn.clicked.connect(self.player.play)
        self.pause_btn.clicked.connect(self.player.pause)
        self.stop_btn.clicked.connect(self.player.stop)
        self.add_btn.clicked.connect(self.add_file)

        self.player.positionChanged.connect(self.update_slider)
        self.player.durationChanged.connect(self.set_duration)
        self.player.currentMediaChanged.connect(self.update_label)

    def add_file(self):
          files, _ = QFileDialog.getOpenFileNames(self,"Select Audio Files", "", "Audio Files (*.mp3 *.wav)")
          for file in files:
               self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(file)))
               self.current_label.setText(f"Added: {file.split('/')[-1]}")

    def set_position(self, position):
         self.player.setPosition(position)

    def update_slider(self, position):
         self.slider.setValue(position)

    def set_duration(self, duration):
         self.slider.setRange(0, duration)

    def update_label(self, media):
         if media.isNull():
              self.current_label.setText("No file playing")
         else:
              self.current_label.setText(f"Playing: {media.canonicalUrl().fileName()}")

if __name__ =="__main__":
    app = QApplication(sys.argv)
    window = SimpleMediaPlayer()
    window.show()
    sys.exit(app.exec_())

              