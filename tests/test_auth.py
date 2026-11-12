from unittest.mock import MagicMock, patch
from models.user_model import UserModel

def test_hash_password_sha256():
    pwd_asli = "admin123"
    hash_1 = UserModel.hash_password(pwd_asli)
    hash_2 = UserModel.hash_password(pwd_asli)

    assert hash_1 != pwd_asli
    assert hash_1 == hash_2
    assert len(hash_1) == 64

@patch("models.user_model.get_connection")
def test_autentikasi_berhasil(mock_get_conn):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {
        "id_user": 1,
        "nama": "Admin Badminton",
        "email": "admin@example.com",
        "role": "admin"
    }
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    hasil = UserModel.autentikasi("admin@example.com", "admin123")
    assert hasil is not None
    assert hasil["role"] == "admin"
    mock_cursor.execute.assert_called_once()