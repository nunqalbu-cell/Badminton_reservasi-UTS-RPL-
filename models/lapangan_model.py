import mysql.connector
from config.database import get_connection


class LapanganModel:
    @staticmethod
    def get_all_lapangan():
        """Mengambil seluruh data master lapangan dari tabel lapangan."""
        conn = get_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT id_lapangan, nama_lapangan, harga_per_jam,
                       status_lapangan, keterangan
                FROM lapangan
                ORDER BY id_lapangan ASC
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception:
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_lapangan(nama_lapangan, harga_per_jam, status_lapangan="aktif", keterangan=""):
        """Menambahkan fasilitas lapangan baru oleh Admin."""
        conn = get_connection()
        if not conn:
            return False, "Gagal terhubung ke basis data MySQL."
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO lapangan
                (nama_lapangan, harga_per_jam, status_lapangan, keterangan)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (nama_lapangan, harga_per_jam, status_lapangan, keterangan),
            )
            conn.commit()
            return True, f"Lapangan '{nama_lapangan}' berhasil ditambahkan!"
        except Exception as exc:
            conn.rollback()
            return False, f"Gagal menambah lapangan: {exc}"
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_lapangan(
        id_lapangan, nama_lapangan, harga_per_jam, status_lapangan, keterangan=""
    ):
        """Memperbarui data master lapangan berdasarkan ID oleh Admin."""
        conn = get_connection()
        if not conn:
            return False, "Gagal terhubung ke basis data MySQL."
        cursor = conn.cursor()
        try:
            query = """
                UPDATE lapangan
                SET nama_lapangan = %s,
                    harga_per_jam = %s,
                    status_lapangan = %s,
                    keterangan = %s
                WHERE id_lapangan = %s
            """
            cursor.execute(
                query,
                (nama_lapangan, harga_per_jam, status_lapangan, keterangan, id_lapangan),
            )
            conn.commit()
            return True, f"Data lapangan ID {id_lapangan} berhasil diperbarui!"
        except Exception as exc:
            conn.rollback()
            return False, f"Gagal memperbarui lapangan: {exc}"
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_lapangan(id_lapangan):
        """Menghapus data master lapangan berdasarkan ID oleh Admin."""
        conn = get_connection()
        if not conn:
            return False, "Gagal terhubung ke basis data MySQL."
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM lapangan WHERE id_lapangan = %s",
                (id_lapangan,),
            )
            conn.commit()
            return True, f"Data lapangan ID {id_lapangan} berhasil dihapus!"
        except mysql.connector.IntegrityError:
            conn.rollback()
            return (
                False,
                "Lapangan tidak dapat dihapus karena masih digunakan pada data reservasi.",
            )
        except Exception as exc:
            conn.rollback()
            return False, f"Gagal menghapus lapangan: {exc}"
        finally:
            cursor.close()
            conn.close()