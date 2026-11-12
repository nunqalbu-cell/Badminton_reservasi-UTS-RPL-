import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from models.user_model import UserModel
from views.signin_view import SigninView

# Palet Warna: Putih, Biru Navy, dan Hijau Rumput
COLOR_BG = "#F4F6F9"
COLOR_WHITE = "#FFFFFF"
COLOR_NAVY = "#0F2C59"
COLOR_NAVY_HOVER = "#091D3E"
COLOR_GREEN = "#2E7D32"
COLOR_GREEN_HOVER = "#1B5E20"
COLOR_BORDER = "#D0D7DE"


def get_asset_path(filename):
    """Mendukung pembacaan aset baik saat dijalankan via Python maupun file .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'assets', filename)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', filename))


class LoginView(ctk.CTk):
    def __init__(self, on_login_success=None):
        super().__init__()
        self.on_login_success = on_login_success

        # Paksa Mode Terang (Light Mode)
        ctk.set_appearance_mode("Light")
        self.title("Login - Sistem Reservasi Lapangan Badminton")
        self.geometry("420x500")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG)

        # Posisikan jendela di tengah layar
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 210
        y = (self.winfo_screenheight() // 2) - 250
        self.geometry(f"420x500+{x}+{y}")

        # Ubah ikon pojok kiri atas & Taskbar (mengganti ikon 'C' biru CustomTkinter)
        ico_path = get_asset_path("logo.ico")
        if os.path.exists(ico_path):
            self.iconbitmap(ico_path)
            self.after(300, lambda: self.iconbitmap(ico_path))

        # Container Kartu Putih
        self.frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_WHITE,
            corner_radius=15,
            border_width=1,
            border_color=COLOR_BORDER
        )
        self.frame.pack(fill="both", expand=True, padx=25, pady=25)

        # Logo Aplikasi di atas Form Login
        logo_path = get_asset_path("logo.png")
        if not os.path.exists(logo_path):
            logo_path = get_asset_path("logo.jpeg")

        if os.path.exists(logo_path):
            img = Image.open(logo_path)
            self.logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(120, 70))
            self.lbl_logo = ctk.CTkLabel(self.frame, image=self.logo_img, text="")
        else:
            self.lbl_logo = ctk.CTkLabel(self.frame, text="🏸", font=ctk.CTkFont(size=52))
        self.lbl_logo.pack(pady=(22, 5))

        # Judul Biru Navy
        ctk.CTkLabel(
            self.frame,
            text="LOGIN SISTEM",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLOR_NAVY
        ).pack(pady=(2, 2))

        ctk.CTkLabel(
            self.frame,
            text="Reservasi Lapangan Badminton",
            font=ctk.CTkFont(size=12),
            text_color="#555555"
        ).pack(pady=(0, 18))

        # Input Email
        self.entry_email = ctk.CTkEntry(
            self.frame,
            placeholder_text="Masukkan Email",
            height=38,
            fg_color=COLOR_WHITE,
            border_color=COLOR_BORDER,
            text_color="#111111"
        )
        self.entry_email.pack(pady=7, padx=25, fill="x")

        # Input Password
        self.entry_password = ctk.CTkEntry(
            self.frame,
            placeholder_text="Masukkan Password",
            show="*",
            height=38,
            fg_color=COLOR_WHITE,
            border_color=COLOR_BORDER,
            text_color="#111111"
        )
        self.entry_password.pack(pady=7, padx=25, fill="x")

        # Tombol Masuk (Hijau Rumput)
        self.btn_login = ctk.CTkButton(
            self.frame,
            text="Masuk",
            height=38,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=COLOR_GREEN,
            hover_color=COLOR_GREEN_HOVER,
            text_color=COLOR_WHITE,
            command=self.proses_login
        )
        self.btn_login.pack(pady=(16, 8), padx=25, fill="x")

        # Tombol Daftar Akun Baru (Biru Navy)
        self.btn_register = ctk.CTkButton(
            self.frame,
            text="Daftar Akun Pelanggan",
            height=36,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=COLOR_NAVY,
            hover_color=COLOR_NAVY_HOVER,
            text_color=COLOR_WHITE,
            command=self.buka_registrasi
        )
        self.btn_register.pack(pady=(0, 15), padx=25, fill="x")

        # Tekan Enter untuk langsung login
        self.bind("<Return>", lambda event: self.proses_login())

    def proses_login(self):
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()

        if not email or not password:
            messagebox.showwarning("Peringatan", "Email dan Password wajib diisi!")
            return

        user = UserModel.autentikasi(email, password)
        if user:
            nama = user.get("nama", email) if isinstance(user, dict) else email
            role = user.get("role", "pelanggan") if isinstance(user, dict) else "pelanggan"
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {nama} ({role.upper()})!")
            if self.on_login_success:
                self.on_login_success(user)
        else:
            messagebox.showerror("Login Gagal", "Email atau Password salah!")

    def buka_registrasi(self):
        SigninView(self)


if __name__ == "__main__":
    app = LoginView(on_login_success=lambda u: print("Login:", u))
    app.mainloop()