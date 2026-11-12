import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.pembayaran_controller import PembayaranController

# Palet Warna Tema: Putih, Biru Navy, dan Hijau Rumput
COLOR_BG = "#F4F6F9"
COLOR_WHITE = "#FFFFFF"
COLOR_NAVY = "#0F2C59"
COLOR_NAVY_HOVER = "#071E3D"
COLOR_GRASS_GREEN = "#2E7D32"
COLOR_GREEN_HOVER = "#1B5E20"
COLOR_RED = "#DC3545"
COLOR_BORDER = "#D0D7DE"


class PembayaranView(ctk.CTkFrame):
    def __init__(self, parent, role="pelanggan"):
        super().__init__(parent, fg_color=COLOR_BG)
        self.role = role.lower() if role else "pelanggan"
        self.controller = PembayaranController()
        self.raw_data = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Frame Form Kiri (Kartu Putih)
        self.frame_form = ctk.CTkFrame(
            self,
            fg_color=COLOR_WHITE,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDER
        )
        self.frame_form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            self.frame_form,
            text=f"Form Pembayaran ({self.role.capitalize()})",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=COLOR_NAVY
        ).pack(pady=(15, 10))

        self.entry_id_reservasi = ctk.CTkEntry(
            self.frame_form, placeholder_text="ID Reservasi (misal: 1)",
            fg_color=COLOR_WHITE, border_color=COLOR_BORDER, text_color="#111111"
        )
        self.entry_id_reservasi.pack(pady=5, fill="x", padx=15)

        self.combo_metode = ctk.CTkOptionMenu(
            self.frame_form,
            values=["Transfer BCA", "Transfer Mandiri", "QRIS", "E-Wallet DANA", "Tunai"],
            fg_color=COLOR_NAVY,
            button_color=COLOR_NAVY_HOVER,
            button_hover_color=COLOR_NAVY_HOVER,
            text_color=COLOR_WHITE
        )
        self.combo_metode.set("Transfer BCA")
        self.combo_metode.pack(pady=5, fill="x", padx=15)

        self.entry_jumlah = ctk.CTkEntry(
            self.frame_form, placeholder_text="Jumlah Bayar (Rp)",
            fg_color=COLOR_WHITE, border_color=COLOR_BORDER, text_color="#111111"
        )
        self.entry_jumlah.pack(pady=5, fill="x", padx=15)

        self.entry_kode_ref = ctk.CTkEntry(
            self.frame_form, placeholder_text="Kode Referensi (opsional)",
            fg_color=COLOR_WHITE, border_color=COLOR_BORDER, text_color="#111111"
        )
        self.entry_kode_ref.pack(pady=5, fill="x", padx=15)

        self.entry_tanggal_bayar = ctk.CTkEntry(
            self.frame_form, placeholder_text="Tgl Bayar (YYYY-MM-DD HH:MM:SS)",
            fg_color=COLOR_WHITE, border_color=COLOR_BORDER, text_color="#111111"
        )
        self.entry_tanggal_bayar.pack(pady=5, fill="x", padx=15)

        # Pengaturan Status Pembayaran Berdasarkan Role (RBAC)
        if self.role == "admin":
            self.combo_status = ctk.CTkOptionMenu(
                self.frame_form,
                values=["menunggu", "lunas", "gagal"],
                fg_color=COLOR_NAVY,
                button_color=COLOR_NAVY_HOVER,
                button_hover_color=COLOR_NAVY_HOVER,
                text_color=COLOR_WHITE
            )
            self.combo_status.set("menunggu")
            self.combo_status.pack(pady=6, fill="x", padx=15)
        else:
            self.lbl_status_info = ctk.CTkLabel(
                self.frame_form,
                text="Status: menunggu (Menunggu Verifikasi Admin)",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=COLOR_GRASS_GREEN
            )
            self.lbl_status_info.pack(pady=6, fill="x", padx=15)

        # Tombol Simpan (Hijau Rumput - Semua Role)
        self.btn_simpan = ctk.CTkButton(
            self.frame_form,
            text="Simpan Pembayaran",
            font=ctk.CTkFont(weight="bold"),
            fg_color=COLOR_GRASS_GREEN,
            hover_color=COLOR_GREEN_HOVER,
            text_color=COLOR_WHITE,
            command=self.simpan_data
        )
        self.btn_simpan.pack(pady=(12, 5), fill="x", padx=15)

        # Tombol Perbarui & Hapus (Khusus Admin)
        if self.role == "admin":
            self.btn_update = ctk.CTkButton(
                self.frame_form,
                text="Perbarui Pembayaran",
                font=ctk.CTkFont(weight="bold"),
                fg_color=COLOR_NAVY,
                hover_color=COLOR_NAVY_HOVER,
                text_color=COLOR_WHITE,
                command=self.update_data
            )
            self.btn_update.pack(pady=4, fill="x", padx=15)

            self.btn_delete = ctk.CTkButton(
                self.frame_form,
                text="Hapus Pembayaran",
                font=ctk.CTkFont(weight="bold"),
                fg_color=COLOR_RED,
                hover_color="#B71C1C",
                text_color=COLOR_WHITE,
                command=self.delete_data
            )
            self.btn_delete.pack(pady=4, fill="x", padx=15)

        # Frame Tabel Kanan (Kartu Putih)
        self.frame_table = ctk.CTkFrame(
            self,
            fg_color=COLOR_WHITE,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDER
        )
        self.frame_table.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Styling Tabel Treeview (Header Biru Navy, Baris Putih)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=COLOR_WHITE,
            foreground="#111111",
            rowheight=28,
            fieldbackground=COLOR_WHITE,
            bordercolor=COLOR_BORDER,
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background=COLOR_NAVY,
            foreground=COLOR_WHITE,
            font=("Arial", 10, "bold"),
            relief="flat"
        )
        style.map("Treeview", background=[("selected", COLOR_GRASS_GREEN)], foreground=[("selected", COLOR_WHITE)])

        cols = ("ID", "ID Res", "Metode", "Jumlah", "Status", "Kode Ref", "Tgl Bayar")
        self.tree = ttk.Treeview(self.frame_table, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=85, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.load_data()

    def clear_form(self):
        self.entry_id_reservasi.delete(0, 'end')
        self.combo_metode.set("Transfer BCA")
        self.entry_jumlah.delete(0, 'end')
        self.entry_kode_ref.delete(0, 'end')
        self.entry_tanggal_bayar.delete(0, 'end')
        if self.role == "admin" and hasattr(self, 'combo_status'):
            self.combo_status.set("menunggu")

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.raw_data.clear()
        data = self.controller.get_all_pembayaran()
        for d in data:
            pay_id = str(d['id_pembayaran'])
            self.raw_data[pay_id] = d

            kode_disp = d.get('kode_referensi') or "-"
            tgl_disp = str(d['tanggal_bayar']) if d.get('tanggal_bayar') else "-"

            self.tree.insert("", "end", iid=pay_id, values=(
                d['id_pembayaran'],
                d['id_reservasi'],
                d['metode_pembayaran'],
                f"Rp{d['jumlah_bayar']:,.2f}",
                d['status_pembayaran'],
                kode_disp,
                tgl_disp
            ))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            pay_id = selected[0]
            self.selected_id = pay_id

            d = self.raw_data.get(pay_id)
            if d:
                self.entry_id_reservasi.delete(0, 'end')
                self.entry_id_reservasi.insert(0, str(d['id_reservasi']))

                self.combo_metode.set(str(d['metode_pembayaran']))

                self.entry_jumlah.delete(0, 'end')
                self.entry_jumlah.insert(0, str(d['jumlah_bayar']))

                self.entry_kode_ref.delete(0, 'end')
                if d.get('kode_referensi'):
                    self.entry_kode_ref.insert(0, str(d['kode_referensi']))

                self.entry_tanggal_bayar.delete(0, 'end')
                if d.get('tanggal_bayar'):
                    self.entry_tanggal_bayar.insert(0, str(d['tanggal_bayar']))

                if self.role == "admin" and hasattr(self, 'combo_status'):
                    self.combo_status.set(str(d['status_pembayaran']))

    def simpan_data(self):
        id_res = self.entry_id_reservasi.get()
        metode = self.combo_metode.get()
        jumlah = self.entry_jumlah.get().replace("Rp", "").replace(",", "").strip()
        kode_ref = self.entry_kode_ref.get()
        tgl_bayar = self.entry_tanggal_bayar.get()
        status = self.combo_status.get() if self.role == "admin" and hasattr(self, 'combo_status') else "menunggu"

        success, msg = self.controller.add_pembayaran(id_res, metode, jumlah, status, kode_ref, tgl_bayar)
        if success:
            messagebox.showinfo("Sukses", msg)
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", msg)

    def update_data(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showwarning("Peringatan", "Pilih data pembayaran di tabel terlebih dahulu!")
            return

        id_res = self.entry_id_reservasi.get()
        metode = self.combo_metode.get()
        jumlah = self.entry_jumlah.get().replace("Rp", "").replace(",", "").strip()
        kode_ref = self.entry_kode_ref.get()
        tgl_bayar = self.entry_tanggal_bayar.get()
        status = self.combo_status.get() if hasattr(self, 'combo_status') else "menunggu"

        success, msg = self.controller.update_pembayaran(
            self.selected_id, id_res, metode, jumlah, status, kode_ref, tgl_bayar
        )
        if success:
            messagebox.showinfo("Sukses", msg)
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", msg)

    def delete_data(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showwarning("Peringatan", "Pilih data pembayaran di tabel terlebih dahulu!")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data pembayaran ini?"):
            success, msg = self.controller.delete_pembayaran(self.selected_id)
            if success:
                messagebox.showinfo("Sukses", msg)
                self.clear_form()
                if hasattr(self, 'selected_id'):
                    delattr(self, 'selected_id')
                self.load_data()
            else:
                messagebox.showerror("Error", msg)