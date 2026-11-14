import mysql.connector
from config.database import get_connection


class ReservasiModel:
    @staticmethod
    def get_all_reservasi():
        """Mengambil seluruh data transaksi reservasi dari tabel reservasi."""
        conn = get_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT id_reservasi, id_user, id_lapangan,
                       tanggal_reservasi, jam_mulai, jam_selesai,
                       total_harga, status_reservasi
                FROM reservasi
                ORDER BY id_reservasi DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception:
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_reservasi(
        id_user, id_lapangan, tanggal_reservasi, jam_mulai, jam_selesai, total_harga
    ):
        """Menambahkan transaksi reservasi baru dengan validasi ID User & Lapangan."""
        conn = get_connection()
        if not conn:
            return False, "Gagal terhubung ke basis data MySQL."
        cursor = conn.cursor(dictionary=True)
        try:
            # 1. Cek apakah ID User terdaftar
            cursor.execute("SELECT id_user FROM users WHERE id_user = %s", (id_user,))
            if not cursor.fetchone():
                cursor.execute("SELECT id_user, nama FROM users ORDER BY id_user ASC")
                users = cursor.fetchall()
                daftar_u = ", ".join(f"{u['id_user']} ({u['nama']})" for u in users)
                return False, f"ID User {id_user} tidak ditemukan!\nID User tersedia: {daftar_u or 'Kosong'}"

            # 2. Cek apakah ID Lapangan terdaftar
            cursor.execute(
                "SELECT id_lapangan FROM lapangan WHERE id_lapangan = %s",
                (id_lapangan,),
            )
            if not cursor.fetchone():
                cursor.execute(
                    "SELECT id_lapangan, nama_lapangan FROM lapangan ORDER BY id_lapangan ASC"
                )
                laps = cursor.fetchall()
                daftar_l = ", ".join(
                    f"{lap['id_lapangan']} ({lap['nama_lapangan']})" for lap in laps
                )
                return (
                    False,
                    f"ID Lapangan {id_lapangan} tidak ditemukan!\nID Lapangan tersedia: {daftar_l or 'Kosong'}",
                )

            # 3. Simpan data reservasi baru
            query = """
                INSERT INTO reservasi
                (id_user, id_lapangan, tanggal_reservasi, jam_mulai, jam_selesai,
                 total_harga, status_reservasi)
                VALUES (%s, %s, %s, %s, %s, %s, 'menunggu_pembayaran')
            """
            cursor.execute(
                query,
                (
                    id_user,
                    id_lapangan,
                    tanggal_reservasi,
                    jam_mulai,
                    jam_selesai,
                    total_harga,
                ),
            )
            conn.commit()
            return True, "Data reservasi baru berhasil disimpan!"
        except mysql.connector.Error as exc:
            conn.rollback()
            return False, f"Kesalahan database ({exc.errno}): {exc.msg}"
        except Exception as exc:
            conn.rollback()
            return False, f"Gagal menyimpan reservasi: {exc}"
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_reservasi(
        id_reservasi,
        id_user,
        id_lapangan,
        tanggal_reservasi,
        jam_mulai,
        jam_selesai,
        total_harga,
        status_baru,
    ):
        """Memperbarui seluruh data dan status reservasi oleh Admin."""
        conn = get_connection()
        if not conn:
            return False, "Gagal terhubung ke basis data MySQL."
        cursor = conn.cursor()
        try:
            query = """
                UPDATE reservasi
                SET id_user = %s,
                    id_lapangan = %s,
                    tanggal_reservasi = %s,
                    jam_mulai = %s,
                    jam_selesai = %s,
                    total_harga = %s,
                    status_reservasi = %s
                WHERE id_reservasi = %s
            """
            cursor.execute(
                query,
                (
                    id_user,
                    id_lapangan,
                    tanggal_reservasi,
                    jam_mulai,
                    jam_selesai,
                    total_harga,
                    status_baru,
                    id_reservasi,
                ),
            )
            conn.commit()
            return True, f"Data reservasi ID {id_reservasi} berhasil diperbarui!"
        except mysql.connector.Error as exc:
            conn.rollback()
            return False, f"Gagal memperbarui reservasi: {exc.msg}"
        except Exception as exc:
            conn.rollback()
            return False, f"Gagal memperbarui reservasi: {exc}"
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_status_reservasi(id_reservasi, status_baru):
        """Memperbarui hanya status reservasi."""
        conn = get_connection()
        if not conn:
            return False, "Gagal terhubung ke basis data MySQL."
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE reservasi SET status_reservasi = %s WHERE id_reservasi = %s",
                (status_baru, id_reservasi),
            )
            conn.commit()
            return True, f"Status reservasi ID {id_reservasi} diperbarui menjadi '{status_baru}'."
        except Exception as exc:
            conn.rollback()
            return False, f"Gagal memperbarui status reservasi: {exc}"
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_reservasi(id_reservasi):
        """Menghapus riwayat & pembayaran terkait terlebih dahulu, lalu menghapus reservasi."""
        conn = get_connection()
        if not conn:
            return False, "Gagal terhubung ke basis data MySQL."
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM riwayat_reservasi WHERE id_reservasi = %s",
                (id_reservasi,),
            )
            cursor.execute(
                "DELETE FROM pembayaran WHERE id_reservasi = %s",
                (id_reservasi,),
            )
            cursor.execute(
                "DELETE FROM reservasi WHERE id_reservasi = %s",
                (id_reservasi,),
            )
            conn.commit()
            return True, f"Data reservasi ID {id_reservasi} beserta data terkait berhasil dihapus!"
        except Exception as exc:
            conn.rollback()
            return False, f"Gagal menghapus reservasi: {exc}"
        finally:
            cursor.close()
            conn.close()