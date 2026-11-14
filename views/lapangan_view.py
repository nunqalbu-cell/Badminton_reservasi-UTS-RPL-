from tkinter import ttk, messagebox
import customtkinter as ctk
from controllers.lapangan_controller import LapanganController


class LapanganView(ctk.CTkFrame):
    def __init__(self, parent, user_data: dict):
        super().__init__(parent, fg_color="#F4F6F9")
        self.role = user_data.get("role", "pelanggan").lower()
        self.selected_id = None
        self._build_ui()
        self.load_data()

    def _build_ui(self):
        if self.role == "admin":
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=2)
            self.grid_rowconfigure(0, weight=1)
            self._build_admin_form()
            table_col = 1
        else:
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            table_col = 0

        table_card = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#D1D5DB",
        )
        table_card.grid(row=0, column=table_col, sticky="nsew", pady=4)

        top_bar = ctk.CTkFrame(table_card, fg_color="transparent")
        top_bar.pack(fill="x", padx=16, pady=(14, 8))

        ctk.CTkLabel(
            top_bar,
            text="Katalog Fasilitas & Tarif Lapangan Badminton",
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

        cols = ("id", "nama", "harga", "status", "keterangan")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings")
        for col_id, title, width in [
            ("id", "ID", 50),
            ("nama", "Nama Lapangan", 180),
            ("harga", "Tarif / Jam (Rp)", 130),
            ("status", "Status", 100),
            ("keterangan", "Keterangan Fasilitas", 260),
        ]:
            self.tree.heading(col_id, text=title)
            self.tree.column(col_id, width=width, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=16, pady=(0, 14))
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _build_admin_form(self):
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
            text="Kelola Master Lapangan (Admin)",
            font=("Arial", 16, "bold"),
            text_color="#0F2C59",
        ).pack(pady=(14, 10), padx=16, anchor="w")

        self.entry_nama = self._add_field(
            form_card, "Nama Lapangan", "Contoh: Lapangan A (Karpet Vinyl)"
        )
        self.entry_harga = self._add_field(
            form_card, "Harga Sewa per Jam (Rp)", "50000"
        )

        ctk.CTkLabel(
            form_card,
            text="Status Operasional",
            font=("Arial", 11, "bold"),
            text_color="#1F2937",
        ).pack(padx=16, anchor="w")
        self.combo_status = ctk.CTkOptionMenu(
            form_card,
            values=["aktif", "nonaktif"],
            fg_color="#0F2C59",
            button_color="#1E3A8A",
            text_color="#FFFFFF",
        )
        self.combo_status.pack(fill="x", padx=16, pady=(2, 8))

        self.entry_ket = self._add_field(
            form_card, "Keterangan Fasilitas", "Lampu LED, Standar BWF..."
        )

        ctk.CTkButton(
            form_card,
            text="Tambah Lapangan",
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            font=("Arial", 12, "bold"),
            command=self._tambah,
        ).pack(fill="x", padx=16, pady=(8, 4))

        ctk.CTkButton(
            form_card,
            text="Perbarui Lapangan",
            fg_color="#007BFF",
            hover_color="#0056B3",
            font=("Arial", 12, "bold"),
            command=self._update,
        ).pack(fill="x", padx=16, pady=4)

        ctk.CTkButton(
            form_card,
            text="Hapus Lapangan",
            fg_color="#DC3545",
            hover_color="#B02A37",
            font=("Arial", 12, "bold"),
            command=self._hapus,
        ).pack(fill="x", padx=16, pady=4)

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
        for row in LapanganController.get_all_lapangan():
            self.tree.insert(
                "",
                "end",
                values=(
                    row.get("id_lapangan"),
                    row.get("nama_lapangan"),
                    row.get("harga_per_jam"),
                    row.get("status_lapangan"),
                    row.get("keterangan"),
                ),
            )

    def _on_select(self, _event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        self.selected_id = values[0]
        if self.role == "admin":
            self.entry_nama.delete(0, "end")
            self.entry_nama.insert(0, values[1])
            self.entry_harga.delete(0, "end")
            self.entry_harga.insert(0, values[2])
            self.combo_status.set(values[3])
            self.entry_ket.delete(0, "end")
            self.entry_ket.insert(0, values[4] or "")

    def _tambah(self):
        ok, msg = LapanganController.add_lapangan(
            self.entry_nama.get(),
            self.entry_harga.get(),
            self.combo_status.get(),
            self.entry_ket.get(),
        )
        if ok:
            messagebox.showinfo("Berhasil", msg, parent=self)
            self.load_data()
        else:
            messagebox.showerror("Gagal", msg, parent=self)

    def _update(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih lapangan dulu!", parent=self)
            return
        ok, msg = LapanganController.update_lapangan(
            self.selected_id,
            self.entry_nama.get(),
            self.entry_harga.get(),
            self.combo_status.get(),
            self.entry_ket.get(),
        )
        if ok:
            messagebox.showinfo("Berhasil", msg, parent=self)
            self.load_data()
        else:
            messagebox.showerror("Gagal", msg, parent=self)

    def _hapus(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih lapangan dulu!", parent=self)
            return
        if messagebox.askyesno("Konfirmasi", "Hapus data lapangan ini?", parent=self):
            ok, msg = LapanganController.delete_lapangan(self.selected_id)
            if ok:
                messagebox.showinfo("Berhasil", msg, parent=self)
                self.selected_id = None
                self.load_data()
            else:
                messagebox.showerror("Gagal", msg, parent=self)