import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from models.pembayaran_model import PembayaranModel


class PembayaranController:
    def get_all_pembayaran(self):
        try:
            return PembayaranModel.get_all_pembayaran()
        except Exception as e:
            print(f"Error get_all_pembayaran: {e}")
            return []

    def add_pembayaran(self, id_reservasi, metode_pembayaran, jumlah_bayar,
                       status_pembayaran="menunggu", kode_referensi="", tanggal_bayar=""):
        if not str(id_reservasi).strip() or not str(metode_pembayaran).strip() or not str(jumlah_bayar).strip():
            return False, "ID Reservasi, Metode Pembayaran, dan Jumlah Bayar wajib diisi!"

        try:
            id_res_int = int(str(id_reservasi).strip())
            jumlah_float = float(str(jumlah_bayar).strip())
        except ValueError:
            return False, "ID Reservasi dan Jumlah Bayar harus berupa angka!"

        kode_clean = str(kode_referensi).strip() if kode_referensi else None
        tgl_clean = str(tanggal_bayar).strip() if tanggal_bayar else None

        # Otomatis isi waktu bayar saat ini jika status langsung 'lunas' dan tanggal kosong
        if status_pembayaran == "lunas" and not tgl_clean:
            tgl_clean = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            PembayaranModel.add_pembayaran(
                id_res_int, metode_pembayaran.strip(), jumlah_float,
                status_pembayaran, kode_clean, tgl_clean
            )
            return True, "Data pembayaran berhasil disimpan!"
        except Exception as e:
            return False, f"Gagal menyimpan pembayaran: {e}"

    def update_pembayaran(self, id_pembayaran, id_reservasi, metode_pembayaran, jumlah_bayar,
                          status_pembayaran, kode_referensi="", tanggal_bayar=""):
        if not str(id_reservasi).strip() or not str(metode_pembayaran).strip() or not str(jumlah_bayar).strip():
            return False, "ID Reservasi, Metode Pembayaran, dan Jumlah Bayar wajib diisi!"

        try:
            id_pay_int = int(str(id_pembayaran).strip())
            id_res_int = int(str(id_reservasi).strip())
            jumlah_float = float(str(jumlah_bayar).strip())
        except ValueError:
            return False, "ID dan Jumlah Bayar harus berupa angka!"

        kode_clean = str(kode_referensi).strip() if kode_referensi else None
        tgl_clean = str(tanggal_bayar).strip() if tanggal_bayar else None

        # Otomatis isi waktu bayar saat admin mengubah status menjadi 'lunas'
        if status_pembayaran == "lunas" and not tgl_clean:
            tgl_clean = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            PembayaranModel.update_pembayaran(
                id_pay_int, id_res_int, metode_pembayaran.strip(), jumlah_float,
                status_pembayaran, kode_clean, tgl_clean
            )
            return True, "Data pembayaran berhasil diperbarui!"
        except Exception as e:
            return False, f"Gagal memperbarui pembayaran: {e}"

    def delete_pembayaran(self, id_pembayaran):
        try:
            PembayaranModel.delete_pembayaran(int(str(id_pembayaran).strip()))
            return True, "Data pembayaran berhasil dihapus!"
        except Exception as e:
            return False, f"Gagal menghapus pembayaran: {e}"