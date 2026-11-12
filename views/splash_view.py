import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import customtkinter as ctk
from PIL import Image

# Palet Warna Tema: Putih, Biru Navy, dan Hijau Rumput
COLOR_WHITE = "#FFFFFF"
COLOR_NAVY = "#0F2C59"
COLOR_GRASS_GREEN = "#2E7D32"
COLOR_TEXT_SUB = "#555555"


def get_asset_path(filename):
    """Mendukung pembacaan aset baik saat dijalankan via Python maupun file .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'assets', filename)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', filename))


class SplashView(ctk.CTk):
    def __init__(self, on_finish):
        super().__init__()
        self.on_finish = on_finish

        # Paksa Mode Terang (Light Mode)
        ctk.set_appearance_mode("Light")

        self.overrideredirect(True)
        self.geometry("480x320")

        # Posisikan jendela di tengah layar
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 240
        y = (self.winfo_screenheight() // 2) - 160
        self.geometry(f"480x320+{x}+{y}")

        # Atur Ikon Aplikasi
        ico_path = get_asset_path("logo.ico")
        if os.path.exists(ico_path):
            self.after(100, lambda: self.iconbitmap(ico_path))

        # Container Utama (Putih dengan Border Hijau Rumput)
        self.frame = ctk.CTkFrame(
            self,
            corner_radius=15,
            fg_color=COLOR_WHITE,
            border_width=2,
            border_color=COLOR_GRASS_GREEN
        )
        self.frame.pack(fill="both", expand=True)

        # Memuat Gambar Logo dari assets/logo.png
        logo_path = get_asset_path("logo.png")
        if os.path.exists(logo_path):
            img = Image.open(logo_path)
            self.logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(95, 95))
            self.lbl_logo = ctk.CTkLabel(self.frame, image=self.logo_img, text="")
        else:
            self.lbl_logo = ctk.CTkLabel(self.frame, text="🏸", font=ctk.CTkFont(size=60))
        self.lbl_logo.pack(pady=(25, 5))

        # Judul Biru Navy & Subtitle
        self.lbl_title = ctk.CTkLabel(
            self.frame,
            text="BADMINTON RESERVATION SYSTEM",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLOR_NAVY
        )
        self.lbl_title.pack(pady=2)

        self.lbl_sub = ctk.CTkLabel(
            self.frame,
            text="Sistem Informasi Pengelolaan & Reservasi Lapangan",
            font=ctk.CTkFont(size=11),
            text_color=COLOR_TEXT_SUB
        )
        self.lbl_sub.pack(pady=2)

        # Progress Bar Hijau Rumput
        self.progress = ctk.CTkProgressBar(
            self.frame,
            width=340,
            height=8,
            progress_color=COLOR_GRASS_GREEN,
            fg_color="#E0E0E0"
        )
        self.progress.set(0)
        self.progress.pack(pady=20)

        self.after(100, self.start_animation)

    def start_animation(self):
        for i in range(1, 101):
            time.sleep(0.015)
            self.progress.set(i / 100)
            self.update()

        self.destroy()
        if self.on_finish:
            self.on_finish()


if __name__ == "__main__":
    app = SplashView(on_finish=lambda: print("Splash Selesai"))
    app.mainloop()