import tkinter as tk
import customtkinter as ctk
from views.splash_view import SplashView
from views.login_view import LoginView
from views.reservasi_view import DashboardView


def safe_destroy(window):
    """Menghancurkan jendela Tkinter/CTk secara aman tanpa memicu TclError."""
    if window is None:
        return
    try:
        if window.winfo_exists():
            window.destroy()
    except tk.TclError:
        pass


def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # 1. Jalankan Splash Screen (1,5 detik)
    splash = SplashView()
    splash.mainloop()
    was_closed = getattr(splash, "is_closed", False)
    safe_destroy(splash)

    if was_closed:
        return

    # 2. Siklus Login <-> Dashboard (mendukung Logout kembali ke Login)
    while True:
        login_app = LoginView()
        login_app.mainloop()
        user_data = getattr(login_app, "user_data", None)
        safe_destroy(login_app)

        # Keluar aplikasi jika user menutup jendela Login (tombol X)
        if not user_data:
            break

        dashboard_app = DashboardView(user_data)
        dashboard_app.mainloop()
        logout_requested = getattr(dashboard_app, "logout_requested", False)
        safe_destroy(dashboard_app)

        # Jika bukan tombol Logout yang ditekan (tutup jendela X), hentikan program
        if not logout_requested:
            break

if __name__ == "__main__":
    main()