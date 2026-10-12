import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import ttk, messagebox
from views.lapangan_view import LapanganView
from views.pembayaran_view import PembayaranView
from controllers.reservasi_controller import ReservasiController

class DashboardView(ctk.CTk):
    def __init__(self, role="pelanggan", on_logout=None):
        super().__init__()
        self.role = role.lower() if role else "pelanggan"
        self.on_logout = on_logout  # Callback untuk membuka kembali halaman login

        # Judul Jendela menampilkan Hak Akses Aktif
        self.title(f"Sistem Informasi Reservasi Lapangan Badminton - [{self.role.upper()}]")
        self.geometry("1100x650")
        ctk.set_appearance_mode("Dark")

        self.raw_data = {}  # Tempat menyimpan data mentah MySQL

        # Tab Navigation
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_reservasi = self.tabview.add("Kelola Reservasi")
        self.tab_lapangan = self.tabview.add("Katalog Lapangan")
        self.tab_pembayaran = self.tabview.add("Pembayaran")

        # Inisialisasi LapanganView dengan membawa role
        self.view_lapangan = LapanganView(self.tab_lapangan, role=self.role)
        self.view_lapangan.pack(fill="both", expand=True)

        self.view_pembayaran = PembayaranView(self.tab_pembayaran)
        self.view_pembayaran.pack(fill="both", expand=True)

        self.setup_tab_reservasi()

    def setup_tab_reservasi(self):
        self.controller = ReservasiController()

        self.tab_reservasi.grid_columnconfigure(0, weight=1)
        self.tab_reservasi.grid_columnconfigure(1, weight=2)
        self.tab_reservasi.grid_rowconfigure(0, weight=1)

        # Form Kiri
        self.frame_form = ctk.CTkFrame(self.tab_reservasi)
        self.frame_form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_form, text=f"Form Reservasi ({self.role.capitalize()})", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        self.entry_user = ctk.CTkEntry(self.frame_form, placeholder_text="ID User (misal: 1)")
        self.entry_user.pack(pady=5, fill="x", padx=10)

        self.entry_lapangan = ctk.CTkEntry(self.frame_form, placeholder_text="ID Lapangan (misal: 1)")
        self.entry_lapangan.pack(pady=5, fill="x", padx=10)

        self.entry_tanggal = ctk.CTkEntry(self.frame_form, placeholder_text="Tanggal (YYYY-MM-DD)")
        self.entry_tanggal.pack(pady=5, fill="x", padx=10)

        self.entry_jam_mulai = ctk.CTkEntry(self.frame_form, placeholder_text="Jam Mulai (HH:MM:SS)")
        self.entry_jam_mulai.pack(pady=5, fill="x", padx=10)

        self.entry_jam_selesai = ctk.CTkEntry(self.frame_form, placeholder_text="Jam Selesai (HH:MM:SS)")
        self.entry_jam_selesai.pack(pady=5, fill="x", padx=10)

        self.entry_total = ctk.CTkEntry(self.frame_form, placeholder_text="Total Harga (Rp)")
        self.entry_total.pack(pady=5, fill="x", padx=10)

        self.combo_status = ctk.CTkOptionMenu(self.frame_form, values=["menunggu_pembayaran", "dikonfirmasi", "selesai", "dibatalkan"])
        self.combo_status.set("menunggu_pembayaran")
        self.combo_status.pack(pady=5, fill="x", padx=10)

        # 1. Tombol Simpan (Semua Role Bisa)
        self.btn_simpan = ctk.CTkButton(self.frame_form, text="Simpan Reservasi", fg_color="#28A745", hover_color="#218838", command=self.simpan_data)
        self.btn_simpan.pack(pady=8, fill="x", padx=10)

        # 2. Tombol Perbarui & Hapus HANYA MUNCUL JIKA ROLE ADALAH ADMIN
        if self.role == "admin":
            self.btn_update = ctk.CTkButton(self.frame_form, text="Perbarui Data", fg_color="#007BFF", hover_color="#0069D9", command=self.update_data)
            self.btn_update.pack(pady=4, fill="x", padx=10)

            self.btn_delete = ctk.CTkButton(self.frame_form, text="Hapus Data", fg_color="#DC3545", hover_color="#C82333", command=self.delete_data)
            self.btn_delete.pack(pady=4, fill="x", padx=10)

        # 3. Tombol Logout / Keluar (Semua Role Bisa)
        self.btn_logout = ctk.CTkButton(self.frame_form, text="Keluar / Logout", fg_color="#6C757D", hover_color="#5A6268", command=self.logout)
        self.btn_logout.pack(pady=15, fill="x", padx=10)

        # Tabel Kanan
        self.frame_table = ctk.CTkFrame(self.tab_reservasi)
        self.frame_table.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        cols = ("ID", "User", "Lapangan", "Tanggal", "Jam", "Total", "Status")
        self.tree = ttk.Treeview(self.frame_table, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=80)

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.load_data()

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

                self.combo_status.set(d['status_reservasi'])

    def simpan_data(self):
        id_u = self.entry_user.get()
        id_l = self.entry_lapangan.get()
        tgl = self.entry_tanggal.get()
        jm = self.entry_jam_mulai.get()
        js = self.entry_jam_selesai.get()
        tot = self.entry_total.get().replace("Rp", "").replace(",", "").strip()
        st = self.combo_status.get()

        success, msg = self.controller.add_reservasi(id_u, id_l, tgl, jm, js, tot, st)
        if success:
            messagebox.showinfo("Sukses", msg)
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
        st = self.combo_status.get()

        success, msg = self.controller.update_reservasi(self.selected_id, id_u, id_l, tgl, jm, js, tot, st)
        if success:
            messagebox.showinfo("Sukses", msg)
            self.load_data()
        else:
            messagebox.showerror("Error", msg)

    def clear_form(self):
        """Mengosongkan semua isian form input"""
        self.entry_user.delete(0, 'end')
        self.entry_lapangan.delete(0, 'end')
        self.entry_tanggal.delete(0, 'end')
        self.entry_jam_mulai.delete(0, 'end')
        self.entry_jam_selesai.delete(0, 'end')
        self.entry_total.delete(0, 'end')
        self.combo_status.set("menunggu_pembayaran")

    def delete_data(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showwarning("Peringatan", "Pilih data di tabel terlebih dahulu!")
            return
        
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus reservasi ini?"):
            success, msg = self.controller.delete_reservasi(self.selected_id)
            if success:
                messagebox.showinfo("Sukses", msg)
                
                # 1. Bersihkan isian di form sebelah kiri
                self.clear_form()
                
                # 2. Hapus memori id terpilih
                if hasattr(self, 'selected_id'):
                    delattr(self, 'selected_id')
                
                # 3. Muat ulang tabel dari database
                self.load_data()

                # 4. TAMBAHKAN INI: Refresh juga tabel di Tab Pembayaran
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