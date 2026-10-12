import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.database import get_connection

class ReservasiModel:
    @staticmethod
    def get_all_reservasi():
        conn = get_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        
        # Mencegah MySQL membaca data lama dari cache transaksi
        conn.commit()
        
        query = """
            SELECT r.*, u.nama AS nama_user, l.nama_lapangan
            FROM reservasi r
            LEFT JOIN users u ON r.id_user = u.id_user
            LEFT JOIN lapangan l ON r.id_lapangan = l.id_lapangan
            ORDER BY r.id_reservasi DESC
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def add_reservasi(id_user, id_lapangan, tanggal_reservasi, jam_mulai, jam_selesai, total_harga, status_reservasi):
        conn = get_connection()
        if not conn:
            return False, "Koneksi database gagal!"
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO reservasi (id_user, id_lapangan, tanggal_reservasi, jam_mulai, jam_selesai, total_harga, status_reservasi)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (id_user, id_lapangan, tanggal_reservasi, jam_mulai, jam_selesai, total_harga, status_reservasi))
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Reservasi berhasil ditambahkan!"
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            return False, f"Gagal menambahkan reservasi: {e}"

    @staticmethod
    def update_reservasi(id_reservasi, id_user, id_lapangan, tanggal_reservasi, jam_mulai, jam_selesai, total_harga, status_reservasi):
        conn = get_connection()
        if not conn:
            return False, "Koneksi database gagal!"
        try:
            cursor = conn.cursor()
            query = """
                UPDATE reservasi 
                SET id_user=%s, id_lapangan=%s, tanggal_reservasi=%s, jam_mulai=%s, jam_selesai=%s, total_harga=%s, status_reservasi=%s
                WHERE id_reservasi=%s
            """
            cursor.execute(query, (id_user, id_lapangan, tanggal_reservasi, jam_mulai, jam_selesai, total_harga, status_reservasi, id_reservasi))
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Data reservasi berhasil diperbarui!"
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            return False, f"Gagal memperbarui reservasi: {e}"

    @staticmethod
    def delete_reservasi(id_reservasi):
        conn = get_connection()
        if not conn:
            return False, "Koneksi database gagal!"
        try:
            cursor = conn.cursor()
            
            # Matikan pengecekan Foreign Key temporer
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            
            # Hapus data anak di tabel pembayaran & riwayat terlebih dahulu
            cursor.execute("DELETE FROM pembayaran WHERE id_reservasi = %s", (id_reservasi,))
            cursor.execute("DELETE FROM riwayat_reservasi WHERE id_reservasi = %s", (id_reservasi,))
            
            # Hapus data utama di tabel reservasi
            cursor.execute("DELETE FROM reservasi WHERE id_reservasi = %s", (id_reservasi,))
            
            # Nyalakan kembali pengecekan Foreign Key
            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
            
            # Simpan perubahan secara permanen ke MySQL
            conn.commit()
            
            cursor.close()
            conn.close()
            return True, "Data berhasil dihapus!"
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            return False, f"Gagal menghapus: {e}"