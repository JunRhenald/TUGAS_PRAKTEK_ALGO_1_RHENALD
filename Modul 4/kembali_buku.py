import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate
import db_helper

class KembaliBukuWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(KembaliBukuWindow, self).__init__()
        uic.loadUi('kembali_buku.ui', self)
        
        self.dateKembali.setDate(QDate.currentDate())
        
        self.btnKembaliBukuAction.clicked.connect(self.process_return)
        self.btnBersihkan.clicked.connect(self.clear_fields)
        self.btnKeluarForm.clicked.connect(self.close)
        
        self.tableAktif.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        self.load_active_loans_combo()
        self.load_active_loans_table()

    def load_active_loans_combo(self):
        self.cmbPinjam.clear()
        loans = db_helper.get_active_loans()
        for loan in loans:
            id_pinjam, nama_peminjam, id_buku, judul, tgl_pinjam, durasi, status = loan
            self.cmbPinjam.addItem(f"{id_pinjam} - {nama_peminjam} ({judul})", id_pinjam)

    def load_active_loans_table(self):
        self.tableAktif.setRowCount(0)
        loans = db_helper.get_active_loans()
        for row_number, row_data in enumerate(loans):
            self.tableAktif.insertRow(row_number)
            for col_idx in range(6):
                item = QtWidgets.QTableWidgetItem(str(row_data[col_idx]))
                self.tableAktif.setItem(row_number, col_idx, item)

    def process_return(self):
        if self.cmbPinjam.currentIndex() == -1:
            QtWidgets.QMessageBox.warning(self, "Validasi Gagal", "Pilih transaksi peminjaman yang akan dikembalikan!")
            return
            
        id_pinjam = self.cmbPinjam.currentData()
        tanggal_kembali = self.dateKembali.date().toString("yyyy-MM-dd")
        denda = self.spinDenda.value()
        
        success, message = db_helper.return_book(id_pinjam, tanggal_kembali, denda)
        
        if success:
            QtWidgets.QMessageBox.information(self, "Berhasil", message)
            self.load_active_loans_combo()
            self.load_active_loans_table()
            self.clear_fields()
        else:
            QtWidgets.QMessageBox.critical(self, "Gagal", message)

    def clear_fields(self):
        self.dateKembali.setDate(QDate.currentDate())
        self.spinDenda.setValue(0.0)
        if self.cmbPinjam.count() > 0:
            self.cmbPinjam.setCurrentIndex(0)