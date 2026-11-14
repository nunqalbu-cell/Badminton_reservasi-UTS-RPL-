from models.reservasi_model import ReservasiModel


class ReservasiController:
    @staticmethod
    def get_all_reservasi():
        return ReservasiModel.get_all_reservasi()

    @staticmethod
    def add_reservasi(id_user, id_lapangan, tanggal, jam_mulai, jam_selesai, total_harga):
        if not all([
            str(id_user).strip(),
            str(id_lapangan).strip(),
            str(tanggal).strip(),
            str(jam_mulai).strip(),
            str(jam_selesai).strip(),
            str(total_harga).strip(),
        ]):
            return False, "Seluruh kolom formulir reservasi wajib diisi!"

        try:
            uid = int(id_user)
            lid = int(id_lapangan)
            total = float(total_harga)
            if total <= 0:
                return False, "Total biaya harus lebih dari 0!"
        except ValueError:
            return False, "ID User, ID Lapangan, dan Total Biaya harus berupa angka!"

        return ReservasiModel.add_reservasi(
            uid,
            lid,
            str(tanggal).strip(),
            str(jam_mulai).strip(),
            str(jam_selesai).strip(),
            total,
        )

    @staticmethod
    def update_reservasi(
        id_reservasi,
        id_user,
        id_lapangan,
        tanggal,
        jam_mulai,
        jam_selesai,
        total_harga,
        status_baru,
    ):
        if not str(id_reservasi).strip():
            return False, "Pilih baris reservasi pada tabel terlebih dahulu!"
        if not all([
            str(id_user).strip(),
            str(id_lapangan).strip(),
            str(tanggal).strip(),
            str(jam_mulai).strip(),
            str(jam_selesai).strip(),
            str(total_harga).strip(),
        ]):
            return False, "Seluruh kolom formulir wajib diisi sebelum memperbarui!"

        try:
            rid = int(id_reservasi)
            uid = int(id_user)
            lid = int(id_lapangan)
            total = float(total_harga)
        except ValueError:
            return False, "ID User, ID Lapangan, dan Total Biaya harus berupa angka!"

        return ReservasiModel.update_reservasi(
            rid,
            uid,
            lid,
            str(tanggal).strip(),
            str(jam_mulai).strip(),
            str(jam_selesai).strip(),
            total,
            status_baru,
        )

    @staticmethod
    def delete_reservasi(id_reservasi):
        if not str(id_reservasi).strip():
            return False, "Pilih baris reservasi yang akan dihapus!"
        return ReservasiModel.delete_reservasi(int(id_reservasi))