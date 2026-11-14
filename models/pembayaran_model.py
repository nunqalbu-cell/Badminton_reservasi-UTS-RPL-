from config.database import get_connection

class PembayaranModel:
    @staticmethod
    def get_all_pembayaran():
        conn = get_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT id_pembayaran, id_reservasi, metode_pembayaran,
                       jumlah_bayar, status_pembayaran, kode_referensi, tanggal_bayar
                FROM pembayaran
                ORDER BY id_pembayaran DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_pembayaran(id_reservasi, metode, jumlah_bayar, kode_referensi=""):
        conn = get_connection()
        if not conn:
            return False, "Koneksi database gagal."
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO pembayaran
                (id_reservasi, metode_pembayaran, jumlah_bayar, status_pembayaran, kode_referensi)
                VALUES (%s, %s, %s, 'menunggu', %s)
            """
            cursor.execute(query, (id_reservasi, metode, jumlah_bayar, kode_referensi))
            conn.commit()
            return True, "Data pembayaran berhasil dicatat (Menunggu Verifikasi)."
        except Exception as exc:
            conn.rollback()
            return False, f"Gagal menyimpan pembayaran: {exc}"
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_pembayaran(id_pembayaran, status_pembayaran):
        conn = get_connection()
        if not conn:
            return False, "Koneksi database gagal."
        cursor = conn.cursor()
        try:
            if status_pembayaran == "lunas":
                query = """
                    UPDATE pembayaran
                    SET status_pembayaran = %s, tanggal_bayar = NOW()
                    WHERE id_pembayaran = %s
                """
            else:
                query = """
                    UPDATE pembayaran
                    SET status_pembayaran = %s
                    WHERE id_pembayaran = %s
                """
            cursor.execute(query, (status_pembayaran, id_pembayaran))
            conn.commit()
            return True, f"Status pembayaran diperbarui menjadi '{status_pembayaran}'."
        except Exception as exc:
            conn.rollback()
            return False, f"Gagal memperbarui pembayaran: {exc}"
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_pembayaran(id_pembayaran):
        conn = get_connection()
        if not conn:
            return False, "Koneksi database gagal."
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM pembayaran WHERE id_pembayaran = %s",
                (id_pembayaran,),
            )
            conn.commit()
            return True, "Data pembayaran berhasil dihapus."
        except Exception as exc:
            conn.rollback()
            return False, f"Gagal menghapus pembayaran: {exc}"
        finally:
            cursor.close()
            conn.close()