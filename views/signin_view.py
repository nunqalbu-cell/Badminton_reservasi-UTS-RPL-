from tkinter import messagebox
import customtkinter as ctk
from controllers.signin_controller import SigninController


class SigninView(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registrasi Akun Pelanggan")
        self.configure(fg_color="#F4F6F9")
        self.resizable(False, False)

        width, height = 430, 500
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        pos_x = (screen_w - width) // 2
        pos_y = (screen_h - height) // 2
        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

        self.transient(parent)
        self.grab_set()
        self._build_ui()

    def _build_ui(self):
        card = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=16,
            border_width=1,
            border_color="#D1D5DB",
        )
        card.pack(fill="both", expand=True, padx=24, pady=20)

        ctk.CTkLabel(
            card,
            text="PENDAFTARAN PELANGGAN",
            font=("Arial", 18, "bold"),
            text_color="#0F2C59",
        ).pack(pady=(18, 2))

        ctk.CTkLabel(
            card,
            text="Peran Akun Otomatis: Pelanggan (User)",
            font=("Arial", 11, "bold"),
            text_color="#2E7D32",
        ).pack(pady=(0, 14))

        fields = [
            ("Nama Lengkap", "entry_nama", "Masukkan nama lengkap...", False),
            ("Alamat Email", "entry_email", "contoh@email.com", False),
            ("Kata Sandi", "entry_pwd", "Minimal 4 karakter...", True),
            ("Nomor HP / WhatsApp", "entry_nohp", "08xxxxxxxxxx", False),
        ]

        for label_text, attr_name, placeholder, is_secret in fields:
            ctk.CTkLabel(
                card,
                text=label_text,
                font=("Arial", 12, "bold"),
                text_color="#1F2937",
                anchor="w",
            ).pack(fill="x", padx=28)

            entry = ctk.CTkEntry(
                card,
                placeholder_text=placeholder,
                show="*" if is_secret else "",
                height=36,
                fg_color="#F9FAFB",
                border_color="#CBD5E1",
                text_color="#111827",
            )
            entry.pack(fill="x", padx=28, pady=(3, 10))
            setattr(self, attr_name, entry)

        self.btn_submit = ctk.CTkButton(
            card,
            text="Daftar Sekarang",
            height=38,
            font=("Arial", 13, "bold"),
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            text_color="#FFFFFF",
            command=self._handle_register,
        )
        self.btn_submit.pack(fill="x", padx=28, pady=(8, 8))

        ctk.CTkButton(
            card,
            text="Batal / Kembali ke Login",
            height=36,
            font=("Arial", 12),
            fg_color="#6C757D",
            hover_color="#4B5563",
            text_color="#FFFFFF",
            command=self.destroy,
        ).pack(fill="x", padx=28)

    def _handle_register(self):
        success, message = SigninController.register(
            self.entry_nama.get(),
            self.entry_email.get(),
            self.entry_pwd.get(),
            self.entry_nohp.get(),
        )
        if success:
            messagebox.showinfo("Registrasi Berhasil", message, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Registrasi Gagal", message, parent=self)