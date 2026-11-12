import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox
from controllers.signin_controller import SigninController

COLOR_WHITE = "#FFFFFF"
COLOR_NAVY = "#0F2C59"
COLOR_GRASS_GREEN = "#2E7D32"

class SigninView(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Registrasi Akun Pelanggan")
        self.geometry("400x450")
        ctk.set_appearance_mode("Light")
        self.configure(fg_color="#F4F6F9")

        self.controller = SigninController()

        self.frame = ctk.CTkFrame(self, fg_color=COLOR_WHITE, corner_radius=12, border_width=1, border_color="#E0E0E0")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            self.frame, text="DAFTAR AKUN PELANGGAN",
            font=ctk.CTkFont(size=17, weight="bold"), text_color=COLOR_NAVY
        ).pack(pady=(20, 15))

        self.entry_nama = ctk.CTkEntry(self.frame, placeholder_text="Nama Lengkap")
        self.entry_nama.pack(pady=7, fill="x", padx=25)

        self.entry_email = ctk.CTkEntry(self.frame, placeholder_text="Email")
        self.entry_email.pack(pady=7, fill="x", padx=25)

        self.entry_password = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*")
        self.entry_password.pack(pady=7, fill="x", padx=25)

        self.entry_nohp = ctk.CTkEntry(self.frame, placeholder_text="No HP (Opsional)")
        self.entry_nohp.pack(pady=7, fill="x", padx=25)

        self.btn_submit = ctk.CTkButton(
            self.frame, text="Daftar Sekarang",
            fg_color=COLOR_GRASS_GREEN, hover_color="#1B5E20",
            command=self.handle_register
        )
        self.btn_submit.pack(pady=20, fill="x", padx=25)

    def handle_register(self):
        nama = self.entry_nama.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()
        nohp = self.entry_nohp.get().strip()

        if not nama or not email or not password:
            messagebox.showwarning("Peringatan", "Nama, Email, dan Password wajib diisi!")
            return

        # Role otomatis terkunci sebagai 'pelanggan'
        success, msg = self.controller.register_user(nama, email, password, nohp, "pelanggan")
        if success:
            messagebox.showinfo("Sukses", msg)
            self.destroy()
        else:
            messagebox.showerror("Error", msg)