from models.pembayaran_model import PembayaranModel


class PembayaranController:
    @staticmethod
    def get_all():
        return PembayaranModel.get_all_pembayaran()

    @staticmethod
    def tambah_pembayaran(id_reservasi, metode, jumlah_bayar, kode_referensi=""):
        if not str(id_reservasi).strip() or not str(jumlah_bayar).strip():
            return False, "ID Reservasi dan Jumlah Bayar wajib diisi!"
        try:
            res_id = int(id_reservasi)
            nominal = float(jumlah_bayar)
            if nominal <= 0:
                return False, "Jumlah bayar harus lebih dari 0!"
        except ValueError:
            return False, "ID Reservasi dan Jumlah Bayar harus berupa angka!"

        return PembayaranModel.add_pembayaran(
            res_id,
            metode,
            nominal,
            str(kode_referensi).strip(),
        )

    @staticmethod
    def perbarui_pembayaran(
        id_pembayaran, id_reservasi, metode, jumlah_bayar, status_baru, kode_referensi=""
    ):
        if not str(id_pembayaran).strip():
            return False, "Pilih transaksi pembayaran pada tabel terlebih dahulu!"
        if not str(id_reservasi).strip() or not str(jumlah_bayar).strip():
            return False, "ID Reservasi dan Jumlah Bayar wajib diisi!"
        try:
            pid = int(id_pembayaran)
            res_id = int(id_reservasi)
            nominal = float(jumlah_bayar)
        except ValueError:
            return False, "ID Reservasi dan Jumlah Bayar harus berupa angka!"

        return PembayaranModel.update_pembayaran_lengkap(
            pid,
            res_id,
            metode,
            nominal,
            status_baru,
            str(kode_referensi).strip(),
        )

    @staticmethod
    def hapus_pembayaran(id_pembayaran):
        if not str(id_pembayaran).strip():
            return False, "Pilih transaksi pembayaran yang akan dihapus!"
        return PembayaranModel.delete_pembayaran(int(id_pembayaran))