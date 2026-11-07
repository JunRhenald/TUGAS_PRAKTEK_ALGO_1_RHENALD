
import sys
from PyQt5.QtWidgets import *

class TemperatureConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konverter Suhu")
        self.setGeometry(300, 300, 300, 150)

        layout = QVBoxLayout()

        self.label_c = QLabel("Celcius:")
        self.input_c = QLineEdit()
        self.input_c.setPlaceholderText("Masukkan suhu Celcius")

        self.label_f = QLabel("Fahrenheit:")
        self.output_f = QLabel("0 °F")
        self.output_f.setStyleSheet("font-size: 16px; font-weight: bold;")

        layout.addWidget(self.label_c)
        layout.addWidget(self.input_c)
        layout.addWidget(self.label_f)
        layout.addWidget(self.output_f)

        self.setLayout(layout)

        # Signal connection
        self.input_c.textChanged.connect(self.convert)

    def convert(self):
        try:
            celcius = float(self.input_c.text())
            fahrenheit = (celcius * 9/5) + 32
            self.output_f.setText(f"{fahrenheit:.2f} °F")

        except ValueError:
            self.output_f.setText("Invalid input")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TemperatureConverter()
    window.show()
    sys.exit(app.exec_())
