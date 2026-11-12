import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import hashlib
from config.database import get_connection

class UserModel:
    @staticmethod
    def hash_password(password):
        """Mengubah plain text password menjadi hash SHA-256"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def autentikasi(email, password):
        """Verifikasi login menggunakan Parameterized Query dan SHA-256"""
        conn = get_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            pwd_hash = UserModel.hash_password(password)
            query = """
                SELECT id_user, nama, email, no_hp, role 
                FROM users 
                WHERE email = %s AND password_hash = %s
            """
            cursor.execute(query, (email, pwd_hash))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return user
        except Exception as e:
            print(f"Error autentikasi: {e}")
            if conn:
                conn.close()
            return None

    @staticmethod
    def register_user(nama, email, password, no_hp="", role="pelanggan"):
        """Registrasi akun baru dengan password terenkripsi SHA-256 dan role terkunci"""
        conn = get_connection()
        if not conn:
            return False, "Koneksi database gagal!"
        try:
            cursor = conn.cursor()
            # Cek apakah email sudah terdaftar
            cursor.execute("SELECT id_user FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return False, "Email sudah terdaftar! Gunakan email lain."

            pwd_hash = UserModel.hash_password(password)
            # Paksa role selalu 'pelanggan' untuk registrasi publik
            safe_role = "pelanggan"

            query = """
                INSERT INTO users (nama, email, password_hash, no_hp, role)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nama, email, pwd_hash, no_hp, safe_role))
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Registrasi berhasil! Silakan login sebagai Pelanggan."
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            return False, f"Gagal mendaftar: {e}"