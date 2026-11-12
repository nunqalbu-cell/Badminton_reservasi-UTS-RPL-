# 🏸 Sistem Informasi Reservasi Lapangan Badminton

Aplikasi desktop berbasis **Python** untuk pengelolaan jadwal dan reservasi lapangan badminton yang dibangun menggunakan arsitektur **Model-View-Controller (MVC)**, antarmuka modern **CustomTkinter** (tema *Light Mode*: Putih, Navy, dan Hijau Rumput), serta basis data relasional **MySQL**.

Proyek ini dikembangkan untuk memenuhi tugas Praktikum Rekayasa Perangkat Lunak (RPL) 2026 dengan integrasi keamanan autentikasi (**SHA-256**), pembatasan hak akses berbasis peran (**RBAC**), pengujian otomatis (**Pytest**), serta otomatisasi **CI/CD GitHub Actions**.

---

## ✨ Fitur Utama

1. **Splash Screen & Animasi Masuk**
   * Menampilkan logo resmi aplikasi dan *progress bar* pemuatan sistem sebelum masuk ke halaman autentikasi.
2. **Autentikasi & Enkripsi SHA-256**
   * Verifikasi kredensial pengguna menggunakan kueri berparameter (*Parameterized Query*) untuk mencegah *SQL Injection*.
   * Seluruh kata sandi dienkripsi satu arah menggunakan algoritma **SHA-256** (`hashlib`).
3. **Registrasi Akun Khusus Pelanggan**
   * Pendaftaran akun baru melalui form registrasi secara otomatis mengunci peran pengguna sebagai `pelanggan` demi menjaga keamanan hak akses sistem.
4. **Role-Based Access Control (RBAC)**
   * **Admin:** Akses penuh CRUD (Tambah, Lihat, Perbarui, Hapus) pada data Reservasi, Katalog Lapangan, dan Pembayaran, serta pengelolaan status reservasi.
   * **Pelanggan:** Melihat katalog lapangan dan membuat pengajuan reservasi baru dengan status otomatis `menunggu_pembayaran` (akses ubah/hapus data dikunci).
5. **Automated Testing & CI/CD Pipeline**
   * Pengujian unit terisolasi menggunakan `pytest` dan `unittest.mock` serta pengecekan kualitas kode dengan `flake8` yang berjalan otomatis di **GitHub Actions**.
6. **Standalone Desktop Executable (`.exe`)**
   * Dikemas menggunakan `PyInstaller` sehingga dapat dijalankan langsung di Windows tanpa perlu menginstal interpreter Python.

---

## 🛠️ Teknologi yang Digunakan

* **Bahasa Pemrograman:** Python 3.11+
* **Antarmuka GUI:** CustomTkinter & Pillow (PIL)
* **Basis Data:** MySQL (Laragon) & `mysql-connector-python`
* **Pengujian & Linter:** Pytest, `pytest-cov`, `unittest.mock`, Flake8
* **DevOps & Packaging:** Git, GitHub Actions, PyInstaller

---

## 📂 Struktur Direktori (Arsitektur MVC)

```text
badminton_reservation/
├── .github/
│   └── workflows/
│       └── ci_pipeline.yml          # Konfigurasi CI Pipeline (Flake8 & Pytest)
├── assets/
│   └── logo.png                     # Logo aplikasi untuk Splash Screen
├── config/
│   └── database.py                  # Konfigurasi koneksi database MySQL
├── controllers/
│   ├── lapangan_controller.py       # Pengendali logika data lapangan
│   ├── login_controller.py          # Pengendali proses autentikasi login
│   ├── pembayaran_controller.py     # Pengendali transaksi pembayaran
│   ├── reservasi_controller.py      # Pengendali logika CRUD reservasi
│   └── signin_controller.py         # Pengendali registrasi akun pelanggan
├── models/
│   ├── lapangan_model.py            # Kueri SQL tabel lapangan
│   ├── pembayaran_model.py          # Kueri SQL tabel pembayaran
│   ├── reservasi_model.py           # Kueri SQL tabel reservasi
│   ├── riwayat_reservasi_model.py   # Kueri SQL riwayat transaksi
│   └── user_model.py                # Kueri SQL tabel users & hashing SHA-256
├── tests/
│   ├── test_auth.py                 # Unit test hashing SHA-256 & login
│   └── test_reservasi.py            # Unit test operasi CRUD reservasi
├── views/
│   ├── lapangan_view.py             # Tampilan tab katalog lapangan
│   ├── login_view.py                # Tampilan jendela login pengguna
│   ├── pembayaran_view.py           # Tampilan tab pembayaran
│   ├── reservasi_view.py            # Tampilan dashboard utama & kelola reservasi
│   ├── signin_view.py               # Tampilan jendela registrasi pelanggan
│   └── splash_view.py               # Tampilan animasi pembuka aplikasi
├── .gitignore                       # Daftar berkas/folder yang diabaikan Git
├── main.py                          # Titik masuk utama (Entry Point) aplikasi
├── README.md                        # Dokumentasi teknis proyek
└── requirements.txt                 # Daftar dependensi pustaka Python