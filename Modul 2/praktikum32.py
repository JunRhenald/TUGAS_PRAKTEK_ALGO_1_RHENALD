
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel,
    QVBoxLayout, QWidget, QSplashScreen
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Splash Screen Application")
        self.setGeometry(300, 300, 600, 400)

        # Main UI
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        label = QLabel("Selamat Datang di Aplikasi!")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 18, QFont.Bold))

        layout.addWidget(label)


class SplashScreen(QSplashScreen):
    def __init__(self):
        # Membuat background splash screen
        pixmap = QPixmap(500, 300)
        pixmap.fill(Qt.darkBlue)

        super().__init__(pixmap)

        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.loading_step = 0

        self.showMessage(
            "Memulai aplikasi...",
            Qt.AlignBottom | Qt.AlignCenter,
            Qt.white
        )

        # Timer loading
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_loading)

    def start_loading(self):
        self.show()
        self.timer.start(500)

    def update_loading(self):
        self.loading_step += 1

        messages = [
            "Memuat konfigurasi...",
            "Menyiapkan komponen...",
            "Menghubungkan database...",
            "Hampir selesai..."
        ]

        if self.loading_step <= len(messages):
            self.showMessage(
                messages[self.loading_step - 1],
                Qt.AlignBottom | Qt.AlignCenter,
                Qt.white
            )

            QApplication.processEvents()
        else:
            self.timer.stop()
            self.finish_loading()

    def finish_loading(self):
        self.main_window = MainWindow()
        self.main_window.show()

        self.finish(self.main_window)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Membuat splash screen
    splash = SplashScreen()

    # Menampilkan splash screen sebelum event loop
    splash.start_loading()

    sys.exit(app.exec_())
