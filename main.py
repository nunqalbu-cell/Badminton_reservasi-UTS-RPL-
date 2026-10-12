import sys, os
sys.path.append(os.path.dirname(__file__))

from views.login_view import LoginView
from views.reservasi_view import DashboardView

def show_login():
    def on_login_success(user_data):
        # 1. Deteksi role dari dictionary maupun tuple/list
        user_role = "pelanggan"
        if isinstance(user_data, dict):
            user_role = user_data.get('role', 'pelanggan')
        elif isinstance(user_data, (tuple, list)) and len(user_data) > 0:
            user_role = user_data[-1]

        # 2. Tutup jendela login jika masih ada/belum dihancurkan oleh login_view
        try:
            if login_app.winfo_exists():
                login_app.destroy()
        except Exception:
            pass

        # 3. Buka Dashboard sesuai role
        dashboard_app = DashboardView(role=str(user_role), on_logout=show_login)
        dashboard_app.mainloop()

    # Jalankan jendela Login
    login_app = LoginView(on_login_success=on_login_success)
    login_app.mainloop()

if __name__ == "__main__":
    show_login()