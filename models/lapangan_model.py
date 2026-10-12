import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.database import get_connection

class LapanganModel:
    @staticmethod
    def get_all_lapangan():
        conn = get_connection()
        if not conn: return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM lapangan")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def add_lapangan(nama_lapangan, harga_per_jam, status_lapangan='aktif', keterangan=''):
        conn = get_connection()
        if not conn: return False
        cursor = conn.cursor()
        query = "INSERT INTO lapangan (nama_lapangan, harga_per_jam, status_lapangan, keterangan) VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(query, (nama_lapangan, harga_per_jam, status_lapangan, keterangan))
            conn.commit()
            return True
        except Exception as e:
            print("[Error LapanganModel.add_lapangan]:", e)
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_lapangan(self, id_lapangan, nama, harga, status, keterangan):
        try:
            query = "UPDATE lapangan SET nama_lapangan=%s, harga_per_jam=%s, status_lapangan=%s, keterangan=%s WHERE id_lapangan=%s"
            self.cursor.execute(query, (nama, harga, status, keterangan, id_lapangan))
            self.conn.commit()
            return True, "Data lapangan berhasil diperbarui!"
        except Exception as e:
            self.conn.rollback()
            return False, f"Gagal memperbarui lapangan: {e}"

    @staticmethod
    def delete_lapangan(self, id_lapangan):
        try:
            self.cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            query = "DELETE FROM lapangan WHERE id_lapangan=%s"
            self.cursor.execute(query, (id_lapangan,))
            self.cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
            self.conn.commit()
            return True, "Data lapangan berhasil dihapus!"
        except Exception as e:
            self.conn.rollback()
            self.cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
            return False, f"Gagal menghapus lapangan: {e}"
