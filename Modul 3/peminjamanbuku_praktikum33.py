
import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5.QtCore import Qt, QDate

class LibrarySystem(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "peminjamanbuku.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle("Sistem Peminjaman Buku")
        self.init_db()
        self.setup_ui()

    def init_db(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")
        self.db.setDatabaseName(db_path)

        if not self.db.open():
            QMessageBox.critical(self, "Database Error", self.db.lastError().text())
            sys.exit(1)

        query = QSqlQuery(self.db)

        query.exec("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            stock INTEGER DEFAULT 1
        )
        """)

        query.exec("""
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            borrower TEXT,
            loan_date TEXT,
            return_date TEXT,
            status TEXT DEFAULT 'active'
        )
        """)

    def setup_ui(self):
        # Menghubungkan model buku
        self.book_model = QSqlTableModel(self, self.db)
        self.book_model.setTable("books")
        self.book_model.select()
        self.book_table.setModel(self.book_model)
        self.book_table.setSelectionBehavior(QTableView.SelectRows)

        # Menghubungkan model peminjaman
        self.loan_model = QSqlTableModel(self, self.db)
        self.loan_model.setTable("loans")
        self.loan_model.setFilter("status='active'")
        self.loan_model.select()
        self.loan_table.setModel(self.loan_model)
        self.loan_table.setSelectionBehavior(QTableView.SelectRows)

        self.stock_input.setRange(1, 100)

        # Menghubungkan tombol dengan fungsi
        self.add_book_btn.clicked.connect(self.add_book)
        self.update_book_btn.clicked.connect(self.update_book)
        self.delete_book_btn.clicked.connect(self.delete_book)
        self.book_table.clicked.connect(self.on_book_select)
        self.borrow_btn.clicked.connect(self.borrow_book)
        self.return_btn.clicked.connect(self.return_book)
        self.refresh_btn.clicked.connect(self.refresh_stats)

        # Mengatur tampilan laporan
        self.stats_label.setTextFormat(Qt.RichText)
        self.stats_label.setWordWrap(True)
        self.stats_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.stats_label.setMinimumHeight(150)

        self.load_books_to_combo()
        self.refresh_stats()

    def load_books_to_combo(self):
        self.book_combo.clear()
        query = QSqlQuery(self.db)
        query.exec("SELECT id, title FROM books WHERE stock > 0")

        while query.next():
            self.book_combo.addItem(str(query.value(1)), query.value(0))

    def add_book(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        stock = self.stock_input.value()

        if not title:
            QMessageBox.warning(self, "Peringatan", "Judul buku tidak boleh kosong.")
            return

        query = QSqlQuery(self.db)
        query.prepare("INSERT INTO books (title, author, stock) VALUES (?, ?, ?)")
        query.addBindValue(title)
        query.addBindValue(author)
        query.addBindValue(stock)

        if query.exec():
            self.book_model.select()
            self.load_books_to_combo()
            self.clear_book_form()
            self.refresh_stats()
            QMessageBox.information(self, "Sukses", "Buku berhasil ditambahkan.")
        else:
            QMessageBox.warning(self, "Database Error", query.lastError().text())

    def update_book(self):
        current = self.book_table.currentIndex()

        if current.isValid():
            row = current.row()
            book_id = self.book_model.data(self.book_model.index(row, 0))
            title = self.title_input.text().strip()
            author = self.author_input.text().strip()
            stock = self.stock_input.value()

            if not title:
                QMessageBox.warning(self, "Peringatan", "Judul buku tidak boleh kosong.")
                return

            query = QSqlQuery(self.db)
            query.prepare("UPDATE books SET title = ?, author = ?, stock = ? WHERE id = ?")
            query.addBindValue(title)
            query.addBindValue(author)
            query.addBindValue(stock)
            query.addBindValue(book_id)

            if query.exec():
                self.book_model.select()
                self.load_books_to_combo()
                self.refresh_stats()
                QMessageBox.information(self, "Sukses", "Data buku berhasil diperbarui.")
            else:
                QMessageBox.warning(self, "Database Error", query.lastError().text())

    def delete_book(self):
        current = self.book_table.currentIndex()

        if current.isValid():
            row = current.row()
            book_id = self.book_model.data(self.book_model.index(row, 0))

            query = QSqlQuery(self.db)
            query.prepare("SELECT COUNT(*) FROM loans WHERE book_id = ? AND status = 'active'")
            query.addBindValue(book_id)
            query.exec()
            query.next()

            if query.value(0) > 0:
                QMessageBox.warning(self, "Tidak Bisa Dihapus", "Buku masih memiliki peminjaman aktif.")
                return

            reply = QMessageBox.question(self, "Konfirmasi", "Hapus buku ini?", QMessageBox.Yes | QMessageBox.No)

            if reply == QMessageBox.Yes:
                query = QSqlQuery(self.db)
                query.prepare("DELETE FROM books WHERE id = ?")
                query.addBindValue(book_id)

                if query.exec():
                    self.book_model.select()
                    self.load_books_to_combo()
                    self.clear_book_form()
                    self.refresh_stats()
                    QMessageBox.information(self, "Sukses", "Buku berhasil dihapus.")
                else:
                    QMessageBox.warning(self, "Database Error", query.lastError().text())

    def on_book_select(self, index):
        row = index.row()
        self.title_input.setText(str(self.book_model.data(self.book_model.index(row, 1)) or ""))
        self.author_input.setText(str(self.book_model.data(self.book_model.index(row, 2)) or ""))
        self.stock_input.setValue(int(self.book_model.data(self.book_model.index(row, 3))))

    def clear_book_form(self):
        self.title_input.clear()
        self.author_input.clear()
        self.stock_input.setValue(1)

    def borrow_book(self):
        book_id = self.book_combo.currentData()
        borrower = self.borrower_input.text().strip()

        if not borrower:
            QMessageBox.warning(self, "Peringatan", "Nama peminjam tidak boleh kosong.")
            return

        if book_id is None:
            QMessageBox.warning(self, "Peringatan", "Tidak ada buku yang tersedia untuk dipinjam.")
            return

        today = QDate.currentDate().toString("yyyy-MM-dd")

        if not self.db.transaction():
            QMessageBox.warning(self, "Database Error", self.db.lastError().text())
            return

        query = QSqlQuery(self.db)
        query.prepare("INSERT INTO loans (book_id, borrower, loan_date, status) VALUES (?, ?, ?, 'active')")
        query.addBindValue(book_id)
        query.addBindValue(borrower)
        query.addBindValue(today)

        if not query.exec():
            self.db.rollback()
            QMessageBox.warning(self, "Database Error", query.lastError().text())
            return

        query = QSqlQuery(self.db)
        query.prepare("UPDATE books SET stock = stock - 1 WHERE id = ? AND stock > 0")
        query.addBindValue(book_id)

        if not query.exec() or query.numRowsAffected() == 0:
            self.db.rollback()
            QMessageBox.warning(self, "Peminjaman Gagal", "Stok buku tidak tersedia.")
            return

        if not self.db.commit():
            self.db.rollback()
            QMessageBox.warning(self, "Database Error", self.db.lastError().text())
            return

        self.book_model.select()
        self.loan_model.select()
        self.load_books_to_combo()
        self.borrower_input.clear()
        self.refresh_stats()
        QMessageBox.information(self, "Sukses", f"Buku dipinjam oleh {borrower}")

    def return_book(self):
        current = self.loan_table.currentIndex()

        if current.isValid():
            row = current.row()
            loan_id = self.loan_model.data(self.loan_model.index(row, 0))
            book_id = self.loan_model.data(self.loan_model.index(row, 1))
            today = QDate.currentDate().toString("yyyy-MM-dd")

            if not self.db.transaction():
                QMessageBox.warning(self, "Database Error", self.db.lastError().text())
                return

            query = QSqlQuery(self.db)
            query.prepare("UPDATE loans SET return_date = ?, status = 'returned' WHERE id = ? AND status = 'active'")
            query.addBindValue(today)
            query.addBindValue(loan_id)

            if not query.exec() or query.numRowsAffected() == 0:
                self.db.rollback()
                QMessageBox.warning(self, "Pengembalian Gagal", "Data peminjaman tidak dapat diperbarui.")
                return

            query = QSqlQuery(self.db)
            query.prepare("UPDATE books SET stock = stock + 1 WHERE id = ?")
            query.addBindValue(book_id)

            if not query.exec():
                self.db.rollback()
                QMessageBox.warning(self, "Database Error", query.lastError().text())
                return

            if not self.db.commit():
                self.db.rollback()
                QMessageBox.warning(self, "Database Error", self.db.lastError().text())
                return

            self.book_model.select()
            self.loan_model.select()
            self.load_books_to_combo()
            self.refresh_stats()
            QMessageBox.information(self, "Sukses", "Buku telah dikembalikan.")

    def refresh_stats(self):
        # Menghitung total buku yang tersedia
        query = QSqlQuery(self.db)
        query.exec("SELECT COALESCE(SUM(stock), 0) FROM books")
        query.next()
        available_books = int(query.value(0))
        query.exec("SELECT COUNT(*) FROM loans WHERE status = 'active'")
        query.next()
        active_loans = int(query.value(0))
        total_books = available_books + active_loans

        self.stats_label.setText(f"<h2>Laporan Perpustakaan</h2><p><b>Total Buku:</b> {total_books}</p><p><b>Buku Dipinjam:</b> {active_loans}</p><p><b>Buku Tersedia:</b> {available_books}</p>")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibrarySystem()
    window.show()
    sys.exit(app.exec_())


