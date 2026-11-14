from models.lapangan_model import LapanganModel


class LapanganController:
    @staticmethod
    def get_all_lapangan():
        return LapanganModel.get_all_lapangan()

    @staticmethod
    def add_lapangan(nama_lapangan, harga_per_jam, status_lapangan="aktif", keterangan=""):
        if not str(nama_lapangan).strip() or not str(harga_per_jam).strip():
            return False, "Nama lapangan dan harga sewa per jam wajib diisi!"
        try:
            harga = float(harga_per_jam)
            if harga <= 0:
                return False, "Harga sewa per jam harus lebih dari 0!"
        except ValueError:
            return False, "Harga sewa per jam harus berupa angka!"

        return LapanganModel.add_lapangan(
            str(nama_lapangan).strip(),
            harga,
            status_lapangan,
            str(keterangan).strip(),
        )

    @staticmethod
    def update_lapangan(
        id_lapangan, nama_lapangan, harga_per_jam, status_lapangan, keterangan=""
    ):
        if not str(id_lapangan).strip():
            return False, "Pilih baris lapangan pada tabel terlebih dahulu!"
        if not str(nama_lapangan).strip() or not str(harga_per_jam).strip():
            return False, "Nama lapangan dan harga sewa wajib diisi!"
        try:
            harga = float(harga_per_jam)
            if harga <= 0:
                return False, "Harga sewa per jam harus lebih dari 0!"
        except ValueError:
            return False, "Harga sewa per jam harus berupa angka!"

        return LapanganModel.update_lapangan(
            int(id_lapangan),
            str(nama_lapangan).strip(),
            harga,
            status_lapangan,
            str(keterangan).strip(),
        )

    @staticmethod
    def delete_lapangan(id_lapangan):
        if not str(id_lapangan).strip():
            return False, "Pilih baris lapangan yang akan dihapus!"
        return LapanganModel.delete_lapangan(int(id_lapangan))