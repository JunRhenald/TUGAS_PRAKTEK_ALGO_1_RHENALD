import sys
from PyQt5 import QtWidgets, uic
import db_helper

class LaporanWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LaporanWindow, self).__init__()
        uic.loadUi('laporan.ui', self)
        
        self.btnKembali.clicked.connect(self.close)
        self.tableStatistik.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        self.load_statistics()

    def load_statistics(self):
        # General stats cards
        stats = db_helper.get_general_statistics()
        self.valTotalBuku.setText(str(stats['total_buku']))
        self.valActiveLoans.setText(str(stats['active_loans']))
        self.valTotalDenda.setText(f"Rp {stats['total_denda']:,.0f}")
        
        # Most borrowed books table
        self.tableStatistik.setRowCount(0)
        rows = db_helper.get_most_borrowed_books()
        for row_number, row_data in enumerate(rows):
            self.tableStatistik.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.tableStatistik.setItem(row_number, column_number, item)