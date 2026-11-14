import sys 
from PyQt5 import QtWidgets, uic 
import db_helper 
 
class KelolaBukuWindow(QtWidgets.QMainWindow): 
    def __init__(self): 
        super(KelolaBukuWindow, self).__init__() 
        # Load the UI file directly 
        uic.loadUi('kelola_buku.ui', self) 
         
        # Connect buttons 
        self.btnTambah.clicked.connect(self.add_book) 
        self.btnEdit.clicked.connect(self.edit_book) 
        self.btnHapus.clicked.connect(self.delete_book) 
        self.btnBersihkan.clicked.connect(self.clear_fields) 
        self.btnKembali.clicked.connect(self.close) 
         
        # Connect table selection 
        self.tableBuku.itemSelectionChanged.connect(self.on_table_select) 
         
        # Adjust table headers 
        self.tableBuku.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch) 
         
        # Initial load 
        self.load_books() 
 
    def load_books(self): 
        # Clear existing table data 
        self.tableBuku.setRowCount(0) 
         
        # Fetch from database 
        books = db_helper.get_all_books() 
         
        for row_number, row_data in enumerate(books): 
            self.tableBuku.insertRow(row_number) 
            for column_number, data in enumerate(row_data): 
                # Put in table cell 
                item = QtWidgets.QTableWidgetItem(str(data)) 
                self.tableBuku.setItem(row_number, column_number, item) 
                 
    def on_table_select(self): 
        selected_rows = self.tableBuku.selectionModel().selectedRows() 
        if not selected_rows: 
            return 
         
        row = selected_rows[0].row() 
         
        # Populate text fields 
        self.txtIdBuku.setText(self.tableBuku.item(row, 0).text()) 
        self.txtJudul.setText(self.tableBuku.item(row, 1).text()) 
        self.txtPengarang.setText(self.tableBuku.item(row, 2).text()) 
        self.txtPenerbit.setText(self.tableBuku.item(row, 3).text()) 
        self.txtTahun.setText(self.tableBuku.item(row, 4).text()) 
        self.txtStok.setText(self.tableBuku.item(row, 5).text()) 
         
        # Primary key should be read-only on edit 
        self.txtIdBuku.setReadOnly(True) 
 
    def validate_inputs(self): 
        id_buku = self.txtIdBuku.text().strip() 
        judul = self.txtJudul.text().strip() 
        pengarang = self.txtPengarang.text().strip() 
        penerbit = self.txtPenerbit.text().strip() 
        tahun = self.txtTahun.text().strip() 
        stok = self.txtStok.text().strip() 
         
        if not id_buku or not judul or not pengarang or not penerbit or not tahun or not stok: 
            QtWidgets.QMessageBox.warning(self, "Validasi Gagal", "Semua kolom harus diisi!") 
            return None 
         
        try: 
            tahun_int = int(tahun) 
            stok_int = int(stok) 
            if tahun_int < 0 or stok_int < 0: 
                raise ValueError() 
        except ValueError: 
            QtWidgets.QMessageBox.warning(self, "Validasi Gagal", "Tahun Terbit dan Stok harus berupa angka bulat positif!") 
            return None 
             
        return id_buku, judul, pengarang, penerbit, tahun_int, stok_int 
 
    def add_book(self): 
        validated = self.validate_inputs() 
        if not validated: 
            return 
         
        id_buku, judul, pengarang, penerbit, tahun, stok = validated 
        success, message = db_helper.add_book(id_buku, judul, pengarang, penerbit, tahun, stok) 
         
        if success: 
            QtWidgets.QMessageBox.information(self, "Berhasil", message) 
            self.load_books() 
            self.clear_fields() 
        else: 
            QtWidgets.QMessageBox.critical(self, "Gagal", message) 
 
    def edit_book(self): 
        # Check if ID field is read-only (indicates row selection) 
        if not self.txtIdBuku.isReadOnly(): 
            QtWidgets.QMessageBox.warning(self, "Edit Gagal", "Pilih buku dari tabel terlebih dahulu untuk diedit!") 
            return 
             
        validated = self.validate_inputs() 
        if not validated: 
            return 
             
        id_buku, judul, pengarang, penerbit, tahun, stok = validated 
         
        # Confirm edit 
        reply = QtWidgets.QMessageBox.question( 
            self, "Konfirmasi Edit", f"Apakah Anda yakin ingin memperbarui data buku dengan ID {id_buku}?", 
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No 
        ) 
        if reply != QtWidgets.QMessageBox.Yes: 
            return 
             
        success, message = db_helper.update_book(id_buku, judul, pengarang, penerbit, tahun, stok) 
         
        if success: 
            QtWidgets.QMessageBox.information(self, "Berhasil", message) 
            self.load_books() 
            self.clear_fields() 
        else: 
            QtWidgets.QMessageBox.critical(self, "Gagal", message) 
 
    def delete_book(self): 
        id_buku = self.txtIdBuku.text().strip() 
        if not id_buku or not self.txtIdBuku.isReadOnly(): 
            QtWidgets.QMessageBox.warning(self, "Hapus Gagal", "Pilih buku dari tabel terlebih dahulu untuk dihapus!") 
            return 
             
        reply = QtWidgets.QMessageBox.question( 
            self, "Konfirmasi Hapus", f"Apakah Anda yakin ingin menghapus buku dengan ID {id_buku}?", 
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No 
        ) 
        if reply != QtWidgets.QMessageBox.Yes: 
            return 
             
        success, message = db_helper.delete_book(id_buku) 
         
        if success: 
            QtWidgets.QMessageBox.information(self, "Berhasil", message) 
            self.load_books() 
            self.clear_fields() 
        else: 
            QtWidgets.QMessageBox.critical(self, "Gagal", message) 
 
    def clear_fields(self): 
        # Clear fields 
        self.txtIdBuku.clear() 
        self.txtJudul.clear() 
        self.txtPengarang.clear() 
        self.txtPenerbit.clear() 
        self.txtTahun.clear() 
        self.txtStok.clear() 
         
        # Re-enable edit of primary key 
        self.txtIdBuku.setReadOnly(False) 
        self.tableBuku.clearSelection()