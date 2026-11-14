import hashlib
from config.database import get_connection

class UserModel:
    @staticmethod
    def hash_password(password: str) -> str:
        """Mengenkripsi kata sandi menjadi digest heksadesimal SHA-256."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    def registrasi(nama: str, email: str, password: str, no_hp: str = ""):
        """Mendaftarkan akun baru dengan peran dikunci otomatis sebagai 'pelanggan'."""
        conn = get_connection()
        if not conn:
            return False, "Gagal terhubung ke basis data MySQL."

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id_user FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return False, "Email sudah terdaftar! Gunakan email lain."

            pwd_hash = UserModel.hash_password(password)
            query = """
                INSERT INTO users (nama, email, password_hash, no_hp, role)
                VALUES (%s, %s, %s, %s, 'pelanggan')
            """
            cursor.execute(query, (nama, email, pwd_hash, no_hp))
            conn.commit()
            return True, "Registrasi berhasil! Silakan login sebagai Pelanggan."
        except Exception as exc:
            conn.rollback()
            return False, f"Terjadi kesalahan saat registrasi: {exc}"
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def autentikasi(email: str, password: str):
        """Memverifikasi email dan kecocokan hash SHA-256 kata sandi."""
        conn = get_connection()
        if not conn:
            return None

        cursor = conn.cursor(dictionary=True)
        try:
            pwd_hash = UserModel.hash_password(password)
            query = """
                SELECT id_user, nama, email, no_hp, role
                FROM users
                WHERE email = %s AND password_hash = %s
            """
            cursor.execute(query, (email, pwd_hash))
            return cursor.fetchone()
        except Exception:
            return None
        finally:
            cursor.close()
            conn.close()