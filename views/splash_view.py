import os
import sys
import tkinter as tk
import customtkinter as ctk
from PIL import Image


def get_asset_path(filename: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "assets", filename)
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "assets", filename)
    )


class SplashView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.is_closed = False
        self._after_ids = []
        self._progress = 0.0

        self.title("Reservasi Lapangan Badminton")
        self.configure(fg_color="#F4F6F9")
        self.resizable(False, False)

        width, height = 460, 320
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        pos_x = (screen_w - width) // 2
        pos_y = (screen_h - height) // 2
        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._set_window_icon()
        self._build_ui()

        # Mulai animasi progress bar setelah jendela selesai diinisialisasi
        aid = self.after(100, self._animate_progress)
        self._after_ids.append(aid)

    def _set_window_icon(self):
        try:
            ico_path = get_asset_path("logo.ico")
            if os.path.exists(ico_path) and self.winfo_exists():
                self.iconbitmap(ico_path)
        except Exception:
            pass

    def _build_ui(self):
        card = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=16,
            border_width=2,
            border_color="#2E7D32",
        )
        card.pack(fill="both", expand=True, padx=20, pady=20)

        logo_path = get_asset_path("logo.png")
        if os.path.exists(logo_path):
            img = Image.open(logo_path)
            self.logo_img = ctk.CTkImage(light_image=img, size=(96, 96))
            ctk.CTkLabel(card, image=self.logo_img, text="").pack(pady=(24, 8))

        ctk.CTkLabel(
            card,
            text="SISTEM RESERVASI BADMINTON",
            font=("Arial", 18, "bold"),
            text_color="#0F2C59",
        ).pack(pady=(4, 2))

        ctk.CTkLabel(
            card,
            text="Memuat komponen sistem dan konfigurasi...",
            font=("Arial", 12),
            text_color="#4B5563",
        ).pack(pady=(0, 18))

        self.progress_bar = ctk.CTkProgressBar(
            card,
            width=320,
            height=12,
            progress_color="#2E7D32",
            fg_color="#E5E7EB",
        )
        self.progress_bar.pack(pady=(0, 16))
        self.progress_bar.set(0.0)

    def _animate_progress(self):
        if self.is_closed or not self.winfo_exists():
            return

        self._progress += 0.05
        if self._progress <= 1.0:
            self.progress_bar.set(self._progress)
            aid = self.after(70, self._animate_progress)
            self._after_ids.append(aid)
        else:
            self._cancel_all_after()
            self.quit()

    def _cancel_all_after(self):
        for aid in self._after_ids:
            try:
                self.after_cancel(aid)
            except Exception:
                pass
        self._after_ids.clear()

    def _on_close(self):
        self.is_closed = True
        self._cancel_all_after()
        try:
            self.quit()
        except tk.TclError:
            pass