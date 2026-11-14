import sys 
from PyQt5 import QtWidgets, uic 
from PyQt5.QtCore import QDate 
import db_helper 
 
class PinjamBukuWindow(QtWidgets.QMainWindow): 
    def __init__(self): 
        super(PinjamBukuWindow, self).__init__() 
        # Load UI 
        uic.loadUi('pinjam_buku.ui', self) 
         
        # Set default date to today 
        self.datePinjam.setDate(QDate.currentDate()) 
         
        # Connect buttons 
        self.btnPinjam.clicked.connect(self.borrow_book) 
        self.btnBersihkan.clicked.connect(self.clear_fields) 
        self.btnKembali.clicked.connect(self.close) 
         
        # Adjust table headers 
        self.tablePeminjaman.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch) 
         
        # Initial data loading 
        self.load_books_combo() 
        self.load_active_loans() 
 
    def load_books_combo(self): 
        self.cmbBuku.clear() 
        books = db_helper.get_all_books() 
        for book in books: 
            id_buku, judul, _, _, _, stok = book 
            # Only display books that have stock > 0 
            if stok > 0: 
                self.cmbBuku.addItem(f"{id_buku} - {judul} (Stok: {stok})", id_buku) 
 
    def load_active_loans(self): 
        self.tablePeminjaman.setRowCount(0) 
        loans = db_helper.get_active_loans() 
         
        for row_number, row_data in enumerate(loans): 
            self.tablePeminjaman.insertRow(row_number) 
            for column_number, data in enumerate(row_data): 
                item = QtWidgets.QTableWidgetItem(str(data)) 
                self.tablePeminjaman.setItem(row_number, column_number, item) 
 
    def borrow_book(self): 
        id_pinjam = self.txtIdPinjam.text().strip() 
        nama_peminjam = self.txtNamaPeminjam.text().strip() 
         
        if not id_pinjam or not nama_peminjam: 
            QtWidgets.QMessageBox.warning(self, "Validasi Gagal", "ID Pinjam dan Nama Peminjam harus diisi!") 
            return 
             
        if self.cmbBuku.currentIndex() == -1: 
            QtWidgets.QMessageBox.warning(self, "Validasi Gagal", "Buku harus dipilih!") 
            return 
             
        # Get book ID from custom itemData 
        id_buku = self.cmbBuku.currentData() 
        tanggal_pinjam = self.datePinjam.date().toString("yyyy-MM-dd") 
        durasi = self.spinDurasi.value() 
         
        # Save borrowing transaction 
        success, message = db_helper.add_loan(id_pinjam, nama_peminjam, id_buku, tanggal_pinjam, durasi) 
         
        if success: 
            QtWidgets.QMessageBox.information(self, "Berhasil", message) 
            self.load_active_loans() 
            self.load_books_combo() # refresh stock display 
            self.clear_fields() 
        else: 
            QtWidgets.QMessageBox.critical(self, "Gagal", message) 
 
    def clear_fields(self): 
        self.txtIdPinjam.clear() 
        self.txtNamaPeminjam.clear() 
        self.datePinjam.setDate(QDate.currentDate()) 
        self.spinDurasi.setValue(7) 
        self.cmbBuku.setCurrentIndex(0) if self.cmbBuku.count() > 0 else None