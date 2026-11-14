from tkinter import ttk, messagebox
import customtkinter as ctk
from controllers.pembayaran_controller import PembayaranController


class PembayaranView(ctk.CTkFrame):
    def __init__(self, parent, user_data: dict):
        super().__init__(parent, fg_color="#F4F6F9")
        self.role = user_data.get("role", "pelanggan").lower()
        self.selected_id = None
        self._build_ui()
        self.load_data()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        form_card = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#D1D5DB",
        )
        form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=4)

        ctk.CTkLabel(
            form_card,
            text="Konfirmasi & Verifikasi Pembayaran",
            font=("Arial", 16, "bold"),
            text_color="#0F2C59",
        ).pack(pady=(14, 10), padx=16, anchor="w")

        self.entry_id_res = self._add_field(
            form_card, "ID Reservasi", "Masukkan ID Reservasi..."
        )

        ctk.CTkLabel(
            form_card,
            text="Metode Pembayaran",
            font=("Arial", 11, "bold"),
            text_color="#1F2937",
        ).pack(padx=16, anchor="w")
        self.combo_metode = ctk.CTkOptionMenu(
            form_card,
            values=["QRIS", "Transfer Bank", "E-Wallet", "Tunai"],
            fg_color="#0F2C59",
            button_color="#1E3A8A",
            text_color="#FFFFFF",
        )
        self.combo_metode.pack(fill="x", padx=16, pady=(2, 8))

        self.entry_jumlah = self._add_field(
            form_card, "Jumlah Bayar (Rp)", "100000"
        )
        self.entry_kode = self._add_field(
            form_card, "Kode Referensi / Nomor Resi", "REF-20261118-01"
        )

        ctk.CTkButton(
            form_card,
            text="Catat Pembayaran",
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            font=("Arial", 12, "bold"),
            command=self._tambah_pembayaran,
        ).pack(fill="x", padx=16, pady=(8, 6))

        if self.role == "admin":
            ctk.CTkLabel(
                form_card,
                text="Status Verifikasi (Khusus Admin)",
                font=("Arial", 11, "bold"),
                text_color="#0F2C59",
            ).pack(padx=16, pady=(8, 0), anchor="w")

            self.combo_status = ctk.CTkOptionMenu(
                form_card,
                values=["menunggu", "lunas", "gagal"],
                fg_color="#0F2C59",
                button_color="#1E3A8A",
                text_color="#FFFFFF",
            )
            self.combo_status.pack(fill="x", padx=16, pady=(2, 8))

            ctk.CTkButton(
                form_card,
                text="Perbarui Pembayaran (Admin)",
                fg_color="#007BFF",
                hover_color="#0056B3",
                font=("Arial", 12, "bold"),
                command=self._verifikasi,
            ).pack(fill="x", padx=16, pady=4)

            ctk.CTkButton(
                form_card,
                text="Hapus Pembayaran (Admin)",
                fg_color="#DC3545",
                hover_color="#B02A37",
                font=("Arial", 12, "bold"),
                command=self._hapus,
            ).pack(fill="x", padx=16, pady=4)

        table_card = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#D1D5DB",
        )
        table_card.grid(row=0, column=1, sticky="nsew", pady=4)

        top_bar = ctk.CTkFrame(table_card, fg_color="transparent")
        top_bar.pack(fill="x", padx=16, pady=(14, 8))

        ctk.CTkLabel(
            top_bar,
            text="Riwayat & Status Transaksi Pembayaran",
            font=("Arial", 16, "bold"),
            text_color="#0F2C59",
        ).pack(side="left")

        ctk.CTkButton(
            top_bar,
            text="Muat Ulang",
            width=100,
            fg_color="#0F2C59",
            hover_color="#1E3A8A",
            command=self.load_data,
        ).pack(side="right")

        cols = ("id_pay", "id_res", "metode", "jumlah", "status", "kode", "tgl")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings")
        for col_id, title, width in [
            ("id_pay", "ID", 45),
            ("id_res", "ID Res.", 65),
            ("metode", "Metode", 105),
            ("jumlah", "Jumlah (Rp)", 100),
            ("status", "Status", 95),
            ("kode", "Kode Ref.", 120),
            ("tgl", "Tanggal Bayar", 135),
        ]:
            self.tree.heading(col_id, text=title)
            self.tree.column(col_id, width=width, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=16, pady=(0, 14))
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _add_field(self, parent, label_text, placeholder):
        ctk.CTkLabel(
            parent,
            text=label_text,
            font=("Arial", 11, "bold"),
            text_color="#1F2937",
        ).pack(padx=16, anchor="w")
        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            height=34,
            fg_color="#F9FAFB",
            border_color="#CBD5E1",
            text_color="#111827",
        )
        entry.pack(fill="x", padx=16, pady=(2, 8))
        return entry

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in PembayaranController.get_all():
            self.tree.insert(
                "",
                "end",
                values=(
                    row.get("id_pembayaran"),
                    row.get("id_reservasi"),
                    row.get("metode_pembayaran"),
                    row.get("jumlah_bayar"),
                    row.get("status_pembayaran"),
                    row.get("kode_referensi") or "-",
                    row.get("tanggal_bayar") or "-",
                ),
            )

    def _on_select(self, _event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        self.selected_id = values[0]
        if self.role == "admin":
            self.combo_status.set(values[4])

    def _tambah_pembayaran(self):
        ok, msg = PembayaranController.tambah_pembayaran(
            self.entry_id_res.get(),
            self.combo_metode.get(),
            self.entry_jumlah.get(),
            self.entry_kode.get(),
        )
        if ok:
            messagebox.showinfo("Berhasil", msg, parent=self)
            self.load_data()
        else:
            messagebox.showerror("Gagal", msg, parent=self)

    def _verifikasi(self):
        ok, msg = PembayaranController.verifikasi_pembayaran(
            self.selected_id, self.combo_status.get()
        )
        if ok:
            messagebox.showinfo("Berhasil", msg, parent=self)
            self.load_data()
        else:
            messagebox.showerror("Gagal", msg, parent=self)

    def _hapus(self):
        if not self.selected_id:
            messagebox.showwarning(
                "Peringatan", "Pilih transaksi pembayaran dulu!", parent=self
            )
            return
        if messagebox.askyesno(
            "Konfirmasi Hapus", "Hapus transaksi pembayaran ini?", parent=self
        ):
            ok, msg = PembayaranController.hapus_pembayaran(self.selected_id)
            if ok:
                messagebox.showinfo("Berhasil", msg, parent=self)
                self.selected_id = None
                self.load_data()
            else:
                messagebox.showerror("Gagal", msg, parent=self)