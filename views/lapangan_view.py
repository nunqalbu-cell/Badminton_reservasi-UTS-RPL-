import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.lapangan_controller import LapanganController

class LapanganView(ctk.CTkFrame):
    def __init__(self, parent, role="pelanggan"):
        super().__init__(parent)
        self.role = role.lower() if role else "pelanggan"
        self.controller = LapanganController()
        self.raw_data = {}  # Penampung data mentah dari MySQL

        # Atur Grid Tata Letak berdasarkan Hak Akses
        if self.role == "admin":
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=2)
            self.grid_rowconfigure(0, weight=1)
            self.setup_admin_ui()
        else:
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.setup_pelanggan_ui()

    def setup_admin_ui(self):
        # --- FORM INPUT (KIRI) - DITAMPILKAN UNTUK ADMIN ---
        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_form, text="Kelola Data Lapangan", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        self.entry_nama = ctk.CTkEntry(self.frame_form, placeholder_text="Nama Lapangan")
        self.entry_nama.pack(pady=5, fill="x", padx=10)

        self.entry_harga = ctk.CTkEntry(self.frame_form, placeholder_text="Harga Per Jam (Rp)")
        self.entry_harga.pack(pady=5, fill="x", padx=10)

        self.combo_status = ctk.CTkOptionMenu(self.frame_form, values=["aktif", "nonaktif"])
        self.combo_status.set("aktif")
        self.combo_status.pack(pady=5, fill="x", padx=10)

        self.entry_ket = ctk.CTkEntry(self.frame_form, placeholder_text="Keterangan")
        self.entry_ket.pack(pady=5, fill="x", padx=10)

        # Tombol Aksi Admin
        self.btn_tambah = ctk.CTkButton(self.frame_form, text="Tambah Lapangan", fg_color="#28A745", hover_color="#218838", command=self.tambah_data)
        self.btn_tambah.pack(pady=8, fill="x", padx=10)

        self.btn_update = ctk.CTkButton(self.frame_form, text="Perbarui Lapangan", fg_color="#007BFF", hover_color="#0069D9", command=self.update_data)
        self.btn_update.pack(pady=4, fill="x", padx=10)

        self.btn_delete = ctk.CTkButton(self.frame_form, text="Hapus Lapangan", fg_color="#DC3545", hover_color="#C82333", command=self.delete_data)
        self.btn_delete.pack(pady=4, fill="x", padx=10)

        # --- TABEL KATALOG (KANAN) ---
        self.frame_table = ctk.CTkFrame(self)
        self.frame_table.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.setup_table(self.frame_table)

    def setup_pelanggan_ui(self):
        # --- HANYA TABEL KATALOG (PENUH) UNTUK PELANGGAN ---
        self.frame_table = ctk.CTkFrame(self)
        self.frame_table.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.frame_table, text="Katalog Lapangan Badminton", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        self.setup_table(self.frame_table)

    def setup_table(self, parent_frame):
        cols = ("ID", "Nama Lapangan", "Harga/Jam", "Status", "Keterangan")
        self.tree = ttk.Treeview(parent_frame, columns=cols, show="headings")
        
        for c in cols:
            self.tree.heading(c, text=c)
        
        self.tree.column("ID", width=40)
        self.tree.column("Nama Lapangan", width=150)
        self.tree.column("Harga/Jam", width=100)
        self.tree.column("Status", width=80)
        self.tree.column("Keterangan", width=200)

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Event klik tabel khusus Admin untuk mengisi form otomatis
        if self.role == "admin":
            self.tree.bind("<<TreeviewSelect>>", self.on_select)
            
        self.load_data()

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.raw_data.clear()
        try:
            data = self.controller.get_all_lapangan()
            for d in data:
                lap_id = str(d.get('id_lapangan', ''))
                self.raw_data[lap_id] = d
                
                harga_val = d.get('harga_per_jam', 0)
                harga_fmt = f"Rp{harga_val:,.2f}" if isinstance(harga_val, (int, float)) else str(harga_val)
                
                self.tree.insert("", "end", iid=lap_id, values=(
                    d.get('id_lapangan', ''),
                    d.get('nama_lapangan', ''),
                    harga_fmt,
                    d.get('status_lapangan', ''),
                    d.get('keterangan', '')
                ))
        except Exception as e:
            print(f"Error load data lapangan: {e}")

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            lap_id = selected[0]
            self.selected_id = lap_id
            
            d = self.raw_data.get(lap_id)
            if d:
                self.entry_nama.delete(0, 'end')
                self.entry_nama.insert(0, str(d.get('nama_lapangan', '')))

                self.entry_harga.delete(0, 'end')
                self.entry_harga.insert(0, str(d.get('harga_per_jam', '')))

                self.combo_status.set(d.get('status_lapangan', 'aktif'))

                self.entry_ket.delete(0, 'end')
                self.entry_ket.insert(0, str(d.get('keterangan', '')))

    def tambah_data(self):
        nama = self.entry_nama.get()
        harga = self.entry_harga.get().replace("Rp", "").replace(",", "").strip()
        status = self.combo_status.get()
        ket = self.entry_ket.get()

        if hasattr(self.controller, 'add_lapangan'):
            success, msg = self.controller.add_lapangan(nama, harga, status, ket)
            if success:
                messagebox.showinfo("Sukses", msg)
                self.load_data()
            else:
                messagebox.showerror("Error", msg)

    def update_data(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showwarning("Peringatan", "Pilih data lapangan di tabel terlebih dahulu!")
            return
        
        nama = self.entry_nama.get()
        harga = self.entry_harga.get().replace("Rp", "").replace(",", "").strip()
        status = self.combo_status.get()
        ket = self.entry_ket.get()

        if hasattr(self.controller, 'update_lapangan'):
            success, msg = self.controller.update_lapangan(self.selected_id, nama, harga, status, ket)
            if success:
                messagebox.showinfo("Sukses", msg)
                self.load_data()
            else:
                messagebox.showerror("Error", msg)
        else:
            messagebox.showerror("Error", "Fungsi update_lapangan belum ada di LapanganController!")

    def delete_data(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showwarning("Peringatan", "Pilih data lapangan di tabel terlebih dahulu!")
            return
        
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus lapangan ini?"):
            if hasattr(self.controller, 'delete_lapangan'):
                success, msg = self.controller.delete_lapangan(self.selected_id)
                if success:
                    messagebox.showinfo("Sukses", msg)
                    if hasattr(self, 'selected_id'):
                        delattr(self, 'selected_id')
                    self.load_data()
                else:
                    messagebox.showerror("Error", msg)
            else:
                messagebox.showerror("Error", "Fungsi delete_lapangan belum ada di LapanganController!")