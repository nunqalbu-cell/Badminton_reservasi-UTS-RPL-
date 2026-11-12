from unittest.mock import MagicMock, patch
from models.reservasi_model import ReservasiModel

@patch("models.reservasi_model.get_connection")
def test_get_all_reservasi(mock_get_conn):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {"id_reservasi": 1, "nama_user": "Budi Santoso", "total_harga": 50000.0}
    ]
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    data = ReservasiModel.get_all_reservasi()
    assert len(data) == 1
    assert data[0]["nama_user"] == "Budi Santoso"
    mock_conn.commit.assert_called_once()

@patch("models.reservasi_model.get_connection")
def test_delete_reservasi(mock_get_conn):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    sukses, pesan = ReservasiModel.delete_reservasi(1)
    assert sukses is True
    mock_conn.commit.assert_called_once()