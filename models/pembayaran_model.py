import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config.database as db_mod


def _get_conn():
    """Mengambil koneksi database dari config/database.py secara fleksibel"""
    if hasattr(db_mod, 'get_connection'):
        return db_mod.get_connection()
    if hasattr(db_mod, 'create_connection'):
        return db_mod.create_connection()
    if hasattr(db_mod, 'Database') and hasattr(db_mod.Database, 'get_connection'):
        return db_mod.Database.get_connection()
    if hasattr(db_mod, 'connect'):
        return db_mod.connect()
    raise ImportError("Fungsi koneksi database tidak ditemukan di config/database.py")


class PembayaranModel:
    @staticmethod
    def get_all_pembayaran():
        conn = _get_conn()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM pembayaran ORDER BY id_pembayaran DESC"
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_pembayaran(id_reservasi, metode_pembayaran, jumlah_bayar,
                       status_pembayaran="menunggu", kode_referensi=None, tanggal_bayar=None):
        conn = _get_conn()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO pembayaran
                (id_reservasi, metode_pembayaran, jumlah_bayar, status_pembayaran, kode_referensi, tanggal_bayar)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                id_reservasi,
                metode_pembayaran,
                jumlah_bayar,
                status_pembayaran,
                kode_referensi if kode_referensi else None,
                tanggal_bayar if tanggal_bayar else None
            ))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_pembayaran(id_pembayaran, id_reservasi, metode_pembayaran, jumlah_bayar,
                          status_pembayaran, kode_referensi=None, tanggal_bayar=None):
        conn = _get_conn()
        cursor = conn.cursor()
        try:
            query = """
                UPDATE pembayaran
                SET id_reservasi = %s,
                    metode_pembayaran = %s,
                    jumlah_bayar = %s,
                    status_pembayaran = %s,
                    kode_referensi = %s,
                    tanggal_bayar = %s
                WHERE id_pembayaran = %s
            """
            cursor.execute(query, (
                id_reservasi,
                metode_pembayaran,
                jumlah_bayar,
                status_pembayaran,
                kode_referensi if kode_referensi else None,
                tanggal_bayar if tanggal_bayar else None,
                id_pembayaran
            ))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_pembayaran(id_pembayaran):
        conn = _get_conn()
        cursor = conn.cursor()
        try:
            query = "DELETE FROM pembayaran WHERE id_pembayaran = %s"
            cursor.execute(query, (id_pembayaran,))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()