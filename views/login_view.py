import os
import sys
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
from controllers.login_controller import LoginController
from views.signin_view import SigninView


def get_asset_path(filename: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "assets", filename)
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "assets", filename)
    )


class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.user_data = None
        self._after_ids = []

        self.title("Login — Sistem Reservasi Lapangan Badminton")
        self.configure(fg_color="#F4F6F9")
        self.resizable(False, False)

        width, height = 440, 480
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        pos_x = (screen_w - width) // 2
        pos_y = (screen_h - height) // 2
        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        aid = self.after(150, self._set_window_icon)
        self._after_ids.append(aid)
        self._build_ui()

    def _set_window_icon(self):
        try:
            if not self.winfo_exists():
                return
            ico_path = get_asset_path("logo.ico")
            if os.path.exists(ico_path):
                self.iconbitmap(ico_path)
        except Exception:
            pass

    def _build_ui(self):
        card = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=16,
            border_width=1,
            border_color="#D1D5DB",
        )
        card.pack(fill="both", expand=True, padx=28, pady=24)

        logo_path = get_asset_path("logo.png")
        if os.path.exists(logo_path):
            img = Image.open(logo_path)
            self.logo_img = ctk.CTkImage(light_image=img, size=(76, 76))
            ctk.CTkLabel(card, image=self.logo_img, text="").pack(pady=(20, 6))

        ctk.CTkLabel(
            card,
            text="MASUK KE SISTEM",
            font=("Arial", 20, "bold"),
            text_color="#0F2C59",
        ).pack(pady=(2, 2))

        ctk.CTkLabel(
            card,
            text="Reservasi Lapangan Badminton GOR",
            font=("Arial", 12),
            text_color="#6B7280",
        ).pack(pady=(0, 18))

        ctk.CTkLabel(
            card,
            text="Email",
            font=("Arial", 12, "bold"),
            text_color="#1F2937",
            anchor="w",
        ).pack(fill="x", padx=32)
        self.entry_email = ctk.CTkEntry(
            card,
            placeholder_text="Masukkan email terdaftar...",
            height=38,
            fg_color="#F9FAFB",
            border_color="#CBD5E1",
            text_color="#111827",
        )
        self.entry_email.pack(fill="x", padx=32, pady=(4, 12))

        ctk.CTkLabel(
            card,
            text="Kata Sandi",
            font=("Arial", 12, "bold"),
            text_color="#1F2937",
            anchor="w",
        ).pack(fill="x", padx=32)
        self.entry_password = ctk.CTkEntry(
            card,
            placeholder_text="Masukkan kata sandi...",
            show="*",
            height=38,
            fg_color="#F9FAFB",
            border_color="#CBD5E1",
            text_color="#111827",
        )
        self.entry_password.pack(fill="x", padx=32, pady=(4, 20))
        self.entry_password.bind("<Return>", lambda _event: self._handle_login())

        self.btn_login = ctk.CTkButton(
            card,
            text="Masuk (Login)",
            height=40,
            font=("Arial", 13, "bold"),
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            text_color="#FFFFFF",
            command=self._handle_login,
        )
        self.btn_login.pack(fill="x", padx=32, pady=(0, 10))

        self.btn_signin = ctk.CTkButton(
            card,
            text="Daftar Akun Pelanggan Baru",
            height=38,
            font=("Arial", 12, "bold"),
            fg_color="#0F2C59",
            hover_color="#1E3A8A",
            text_color="#FFFFFF",
            command=self._open_signin,
        )
        self.btn_signin.pack(fill="x", padx=32)

    def _handle_login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        user, message = LoginController.login(email, password)
        if user:
            self.user_data = user
            self._cancel_all_after()
            self.quit()
        else:
            messagebox.showerror("Login Gagal", message, parent=self)

    def _open_signin(self):
        SigninView(self)

    def _cancel_all_after(self):
        for aid in self._after_ids:
            try:
                self.after_cancel(aid)
            except Exception:
                pass
        self._after_ids.clear()

    def _on_close(self):
        self.user_data = None
        self._cancel_all_after()
        try:
            self.quit()
        except tk.TclError:
            pass