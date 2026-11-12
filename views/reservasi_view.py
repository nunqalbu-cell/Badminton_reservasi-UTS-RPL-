import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from views.lapangan_view import LapanganView
from views.pembayaran_view import PembayaranView
from controllers.reservasi_controller import ReservasiController

# Palet Warna Tema: Putih, Biru Navy, dan Hijau Rumput
COLOR_BG = "#F4F6F9"
COLOR_WHITE = "#FFFFFF"
COLOR_NAVY = "#0F2C59"
COLOR_NAVY_HOVER = "#071E3D"
COLOR_GRASS_GREEN = "#2E7D32"
COLOR_GREEN_HOVER = "#1B5E20"
COLOR_RED = "#DC3545"
COLOR_GRAY = "#6C757D"
COLOR_BORDER = "#D0D7DE"


def get_asset_path(filename):
    """Mendukung pembacaan aset baik saat dijalankan via Python maupun file .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'assets', filename)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', filename))


class DashboardView(ctk.CTk):
    def __init__(self, role="pelanggan", on_logout=None):
        super().__init__()
        self.role = role.lower() if role else "pelanggan"
        self.on_logout = on_logout

        # Paksa Mode Terang (Light Mode)
        ctk.set_appearance_mode("Light")
        self.title(f"Sistem Informasi Reservasi Lapangan Badminton - [{self.role.upper()}]")
        self.geometry("1100x650")
        self.configure(fg_color=COLOR_BG)

        # Posisikan jendela di tengah layar
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 550
        y = (self.winfo_screenheight() // 2) - 325
        self.geometry(f"1100x650+{x}+{y}")

        # Timpa ikon bawaan CustomTkinter ('C' biru) setelah 300ms
        self.after(300, self._set_custom_icon)

        self.raw_data = {}

        # Tabview dengan warna aktif Biru Navy
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=COLOR_BG,
            segmented_button_fg_color="#E2E8F0",
            segmented_button_selected_color=COLOR_NAVY,
            segmented_button_selected_hover_color=COLOR_NAVY_HOVER,
            segmented_button_unselected_color="#E2E8F0",
            segmented_button_unselected_hover_color="#CBD5E1",
            text_color=COLOR_WHITE
        )
        self.tabview.pack(fill="both", expand=True, padx=12, pady=12)

        self.tab_reservasi = self.tabview.add("Kelola Reservasi")
        self.tab_lapangan = self.tabview.add("Katalog Lapangan")
        self.tab_pembayaran = self.tabview.add("Pembayaran")

        self.view_lapangan = LapanganView(self.tab_lapangan, role=self.role)
        self.view_lapangan.pack(fill="both", expand=True)

        self.view_pembayaran = PembayaranView(self.tab_pembayaran, role=self.role)
        self.view_pembayaran.pack(fill="both", expand=True)

        self.setup_tab_reservasi()

    def _set_custom_icon(self):
        ico_path = get_asset_path("logo.ico")
        png_path = get_asset_path("logo.png")
        try:
            if os.path.exists(ico_path):
                self.iconbitmap(ico_path)
            if os.path.exists(png_path):
                pil_icon = Image.open(png_path).convert("RGBA")
                self._app_icon = ImageTk.PhotoImage(pil_icon)
                self.wm_iconphoto(True, self._app_icon)
        except Exception:
            pass

    def setup_tab_reservasi(self):
        self.controller = ReservasiController()

        self.tab_reservasi.grid_columnconfigure(0, weight=1)
        self.tab_reservasi.grid_columnconfigure(1, weight=2)
        self.tab_reservasi.grid_rowconfigure(0, weight=1)

        # Frame Form Kiri (Kartu Putih)
        self.frame_form = ctk.CTkFrame(
            self.tab_reservasi,
            fg_color=COLOR_WHITE,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDER
        )
        self.frame_form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            self.frame_form,
            text=f"Form Reservasi ({self.role.capitalize()})",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=COLOR_NAVY
        ).pack(pady=(15, 10))

        self.entry_user = ctk.CTkEntry(
            self.frame_form, placeholder_text="ID User (misal: 1)",
            fg_color=COLOR_WHITE, border_color=COLOR_BORDER, text_color="#111111"
        )
        self.entry_user.pack(pady=5, fill="x", padx=15)

        self.entry_lapangan = ctk.CTkEntry(
            self.frame_form, placeholder_text="ID Lapangan (misal: 1)",
            fg_color=COLOR_WHITE, border_color=COLOR_BORDER, text_color="#111111"
        )
        self.entry_lapangan.pack(pady=5, fill="x", padx=15)

        self.entry_tanggal = ctk.CTkEntry(
            self.frame_form, placeholder_text="Tanggal (YYYY-MM-DD)",
            fg_color=COLOR_WHITE, border_color=COLOR_BORDER, text_color="#111111"
        )
        self.entry_tanggal.pack(pady=5, fill="x", padx=15)

        self.entry_jam_mulai = ctk.CTkEntry(
            self.frame_form, placeholder_text="Jam Mulai (HH:MM:SS)",
            fg_color=COLOR_WHITE, border_color=COLOR_BORDER, text_color="#111111"
        )
        self.entry_jam_mulai.pack(pady=5, fill="x", padx=15)

        self.entry_jam_selesai = ctk.CTkEntry(
            self.frame_form, placeholder_text="Jam Selesai (HH:MM:SS)",
            fg_color=COLOR_WHITE, border_color=COLOR_BORDER, text_color="#111111"
        )
        self.entry_jam_selesai.pack(pady=5, fill="x", padx=15)

        self.entry_total = ctk.CTkEntry(
            self.frame_form, placeholder_text="Total Harga (Rp)",
            fg_color=COLOR_WHITE, border_color=COLOR_BORDER, text_color="#111111"
        )
        self.entry_total.pack(pady=5, fill="x", padx=15)

        # Pengaturan Status Berdasarkan Role (RBAC)
        if self.role == "admin":
            self.combo_status = ctk.CTkOptionMenu(
                self.frame_form,
                values=["menunggu_pembayaran", "dikonfirmasi", "selesai", "dibatalkan"],
                fg_color=COLOR_NAVY,
                button_color=COLOR_NAVY_HOVER,
                button_hover_color=COLOR_NAVY_HOVER,
                text_color=COLOR_WHITE
            )
            self.combo_status.set("menunggu_pembayaran")
            self.combo_status.pack(pady=6, fill="x", padx=15)
        else:
            self.lbl_status_info = ctk.CTkLabel(
                self.frame_form,
                text="Status: menunggu_pembayaran (Otomatis)",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=COLOR_GRASS_GREEN
            )
            self.lbl_status_info.pack(pady=6, fill="x", padx=15)

        # Tombol Simpan (Hijau Rumput)
        self.btn_simpan = ctk.CTkButton(
            self.frame_form,
            text="Simpan Reservasi",
            font=ctk.CTkFont(weight="bold"),
            fg_color=COLOR_GRASS_GREEN,
            hover_color=COLOR_GREEN_HOVER,
            text_color=COLOR_WHITE,
            command=self.simpan_data
        )
        self.btn_simpan.pack(pady=(10, 5), fill="x", padx=15)

        # Tombol Khusus Admin (Perbarui: Biru Navy, Hapus: Merah)
        if self.role == "admin":
            self.btn_update = ctk.CTkButton(
                self.frame_form,
                text="Perbarui Data",
                font=ctk.CTkFont(weight="bold"),
                fg_color=COLOR_NAVY,
                hover_color=COLOR_NAVY_HOVER,
                text_color=COLOR_WHITE,
                command=self.update_data
            )
            self.btn_update.pack(pady=4, fill="x", padx=15)

            self.btn_delete = ctk.CTkButton(
                self.frame_form,
                text="Hapus Data",
                font=ctk.CTkFont(weight="bold"),
                fg_color=COLOR_RED,
                hover_color="#B71C1C",
                text_color=COLOR_WHITE,
                command=self.delete_data
            )
            self.btn_delete.pack(pady=4, fill="x", padx=15)

        # Tombol Logout
        self.btn_logout = ctk.CTkButton(
            self.frame_form,
            text="Keluar / Logout",
            fg_color=COLOR_GRAY,
            hover_color="#545B62",
            text_color=COLOR_WHITE,
            command=self.logout
        )
        self.btn_logout.pack(pady=15, fill="x", padx=15)

        # Frame Tabel Kanan (Kartu Putih)
        self.frame_table = ctk.CTkFrame(
            self.tab_reservasi,
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

        cols = ("ID", "User", "Lapangan", "Tanggal", "Jam", "Total", "Status")
        self.tree = ttk.Treeview(self.frame_table, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=85, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.load_data()

    def clear_form(self):
        self.entry_user.delete(0, 'end')
        self.entry_lapangan.delete(0, 'end')
        self.entry_tanggal.delete(0, 'end')
        self.entry_jam_mulai.delete(0, 'end')
        self.entry_jam_selesai.delete(0, 'end')
        self.entry_total.delete(0, 'end')
        if self.role == "admin" and hasattr(self, 'combo_status'):
            self.combo_status.set("menunggu_pembayaran")

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.raw_data.clear()
        data = self.controller.get_all_reservasi()
        for d in data:
            res_id = str(d['id_reservasi'])
            self.raw_data[res_id] = d

            jam_str = f"{d['jam_mulai']}-{d['jam_selesai']}"
            user_disp = d.get('nama_user') or f"User {d['id_user']}"
            lap_disp = d.get('nama_lapangan') or f"Lap {d['id_lapangan']}"

            self.tree.insert("", "end", iid=res_id, values=(
                d['id_reservasi'], user_disp, lap_disp,
                str(d['tanggal_reservasi']), jam_str,
                f"Rp{d['total_harga']:,.2f}", d['status_reservasi']
            ))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            res_id = selected[0]
            self.selected_id = res_id

            d = self.raw_data.get(res_id)
            if d:
                self.entry_user.delete(0, 'end')
                self.entry_user.insert(0, str(d['id_user']))

                self.entry_lapangan.delete(0, 'end')
                self.entry_lapangan.insert(0, str(d['id_lapangan']))

                self.entry_tanggal.delete(0, 'end')
                self.entry_tanggal.insert(0, str(d['tanggal_reservasi']))

                self.entry_jam_mulai.delete(0, 'end')
                self.entry_jam_mulai.insert(0, str(d['jam_mulai']))

                self.entry_jam_selesai.delete(0, 'end')
                self.entry_jam_selesai.insert(0, str(d['jam_selesai']))

                self.entry_total.delete(0, 'end')
                self.entry_total.insert(0, str(d['total_harga']))

                if self.role == "admin" and hasattr(self, 'combo_status'):
                    self.combo_status.set(d['status_reservasi'])

    def simpan_data(self):
        id_u = self.entry_user.get()
        id_l = self.entry_lapangan.get()
        tgl = self.entry_tanggal.get()
        jm = self.entry_jam_mulai.get()
        js = self.entry_jam_selesai.get()
        tot = self.entry_total.get().replace("Rp", "").replace(",", "").strip()
        st = self.combo_status.get() if self.role == "admin" and hasattr(self, 'combo_status') else "menunggu_pembayaran"

        success, msg = self.controller.add_reservasi(id_u, id_l, tgl, jm, js, tot, st)
        if success:
            messagebox.showinfo("Sukses", msg)
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", msg)

    def update_data(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showwarning("Peringatan", "Pilih data di tabel terlebih dahulu!")
            return

        id_u = self.entry_user.get()
        id_l = self.entry_lapangan.get()
        tgl = self.entry_tanggal.get()
        jm = self.entry_jam_mulai.get()
        js = self.entry_jam_selesai.get()
        tot = self.entry_total.get().replace("Rp", "").replace(",", "").strip()
        st = self.combo_status.get() if hasattr(self, 'combo_status') else "menunggu_pembayaran"

        success, msg = self.controller.update_reservasi(self.selected_id, id_u, id_l, tgl, jm, js, tot, st)
        if success:
            messagebox.showinfo("Sukses", msg)
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", msg)

    def delete_data(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showwarning("Peringatan", "Pilih data di tabel terlebih dahulu!")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus reservasi ini?"):
            success, msg = self.controller.delete_reservasi(self.selected_id)
            if success:
                messagebox.showinfo("Sukses", msg)
                self.clear_form()
                if hasattr(self, 'selected_id'):
                    delattr(self, 'selected_id')

                self.load_data()
                if hasattr(self, 'view_pembayaran') and hasattr(self.view_pembayaran, 'load_data'):
                    self.view_pembayaran.load_data()
            else:
                messagebox.showerror("Error", msg)

    def logout(self):
        if messagebox.askyesno("Konfirmasi Logout", "Apakah Anda yakin ingin keluar dari akun ini?"):
            self.destroy()
            if self.on_logout:
                self.on_logout()


ReservasiView = DashboardView

if __name__ == "__main__":
    app = DashboardView(role="admin")
    app.mainloop()