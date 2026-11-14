from models.user_model import UserModel

class SigninController:
    @staticmethod
    def register(nama: str, email: str, password: str, no_hp: str = ""):
        if not nama.strip() or not email.strip() or not password.strip():
            return False, "Nama lengkap, email, dan kata sandi wajib diisi!"
        if "@" not in email:
            return False, "Format email tidak valid!"
        if len(password.strip()) < 4:
            return False, "Kata sandi minimal 4 karakter!"
        return UserModel.registrasi(
            nama.strip(),
            email.strip(),
            password.strip(),
            no_hp.strip(),
        )