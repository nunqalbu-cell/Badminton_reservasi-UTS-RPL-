from models.user_model import UserModel


class LoginController:
    @staticmethod
    def login(email: str, password: str):
        if not email.strip() or not password.strip():
            return None, "Email dan kata sandi wajib diisi!"
        user = UserModel.autentikasi(email.strip(), password.strip())
        if user:
            return user, "Login berhasil!."
        return None, "Email atau kata sandi salah!"