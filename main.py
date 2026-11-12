import sys, os
sys.path.append(os.path.dirname(__file__))

from views.splash_view import SplashView
from views.login_view import LoginView
from views.reservasi_view import DashboardView

def main():
    def show_login():
        def on_login_success(user_data):
            user_role = "pelanggan"
            if isinstance(user_data, dict):
                user_role = user_data.get('role', 'pelanggan')
            elif isinstance(user_data, (tuple, list)) and len(user_data) > 0:
                user_role = user_data[-1]

            try:
                if login_app.winfo_exists():
                    login_app.destroy()
            except Exception:
                pass

            dashboard_app = DashboardView(role=str(user_role), on_logout=show_login)
            dashboard_app.mainloop()

        login_app = LoginView(on_login_success=on_login_success)
        login_app.mainloop()

    splash = SplashView(on_finish=show_login)
    splash.mainloop()

if __name__ == "__main__":
    main()