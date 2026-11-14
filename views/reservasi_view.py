import os
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from controllers.reservasi_controller import ReservasiController
from views.login_view import get_asset_path
from views.lapangan_view import LapanganView
from views.pembayaran_view import PembayaranView


class DashboardView(ctk.CTk):
    def __init__(self, user_data: dict):
        super().__init__()
        self.user_data = user_data
        self.role = user_data.get("role", "pelanggan").lower()
        self.logout_requested = False
        self._after_ids = []
        self.selected_id = None

        self.title(
            f"Sistem Reservasi Lapangan Badminton — {user_data.get('nama')} ({self.role.upper()})"
        )
        self.configure(fg_color="#F4F6F9")
        self.geometry("1180x670")
        self.minsize(1020, 600)

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        aid = self.after(150, self._set_window_icon)
        self._after_ids.append(aid)

        self._setup_treeview_style()
        self._build_header()
        self._build_tabs()
        self.load_data()

    def _set_window_icon(self):
        try:
            if not self.winfo_exists():
                return
            ico_path = get_asset_path("logo.ico")
            if os.path.exists(ico_path):
                self.iconbitmap(ico_path)
        except Exception:
            pass

    def _setup_treeview_style(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#1F2937",
            rowheight=28,
            fieldbackground="#FFFFFF",
            font=("Arial", 10),
        )
        style.configure(
            "Treeview.Heading",
            background="#0F2C59",
            foreground="#FFFFFF",
            font=("Arial", 10, "bold"),
        )
        style.map("Treeview", background=[("selected", "#2E7D32")])

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="#0F2C59", corner_radius=0, height=54)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="GOR BADMINTON — SISTEM RESERVASI LAPANGAN",
            font=("Arial", 15, "bold"),
            text_color="#FFFFFF",
        ).pack(side="left", padx=20)

        self.btn_logout = ctk.CTkButton(
            header,
            text="Keluar / Logout",
            width=130,
            height=32,
            font=("Arial", 12, "bold"),
            fg_color="#6C757D",
            hover_color="#DC3545",
            text_color="#FFFFFF",
            command=self._handle_logout,
        )
        self.btn_logout.pack(side="right", padx=20)

        info_text = (
            f"ID User: {self.user_data.get('id_user')} | "
            f"{self.user_data.get('nama')} ({self.role.upper()})"
        )
        ctk.CTkLabel(
            header,
            text=info_text,
            font=("Arial", 12, "bold"),
            text_color="#E2E8F0",
        ).pack(side="right", padx=12)

    def _build_tabs(self):
        self.tabview = ctk.CTkTabview(
            self,
            fg_color="#F4F6F9",
            segmented_button_fg_color="#CBD5E1",
            segmented_button_selected_color="#0F2C59",
            segmented_button_selected_hover_color="#1E3A8A",
            segmented_button_unselected_color="#64748B",
            segmented_button_unselected_hover_color="#475569",
            text_color="#FFFFFF",
        )
        self.tabview.pack(fill="both", expand=True, padx=14, pady=(8, 10))
        self.tabview._segmented_button.configure(font=("Arial", 12, "bold"), height=34)

        tab_res = self.tabview.add("Kelola Reservasi")
        tab_lap = self.tabview.add("Katalog Lapangan")
        tab_pay = self.tabview.add("Pembayaran")

        self._build_reservasi_tab(tab_res)
        LapanganView(tab_lap, self.user_data).pack(fill="both", expand=True)
        PembayaranView(tab_pay, self.user_data).pack(fill="both", expand=True)

    def _build_reservasi_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=2)
        parent.grid_rowconfigure(0, weight=1)

        form_outer = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#D1D5DB",
        )
        form_outer.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=2)

        form_card = ctk.CTkScrollableFrame(
            form_outer,
            fg_color="#FFFFFF",
            corner_radius=10,
        )
        form_card.pack(fill="both", expand=True, padx=4, pady=4)

        header_form = ctk.CTkFrame(form_card, fg_color="transparent")
        header_form.pack(fill="x", padx=12, pady=(8, 8))

        ctk.CTkLabel(
            header_form,
            text="Form Pemesanan Lapangan",
            font=("Arial", 15, "bold"),
            text_color="#0F2C59",
        ).pack(side="left")

        ctk.CTkButton(
            header_form,
            text="Bersihkan",
            width=75,
            height=26,
            font=("Arial", 11, "bold"),
            fg_color="#6C757D",
            hover_color="#4B5563",
            command=self._clear_form,
        ).pack(side="right")

        row1 = ctk.CTkFrame(form_card, fg_color="transparent")
        row1.pack(fill="x", padx=12, pady=(0, 6))
        row1.grid_columnconfigure(0, weight=1)
        row1.grid_columnconfigure(1, weight=1)

        col_u = ctk.CTkFrame(row1, fg_color="transparent")
        col_u.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.entry_user = self._add_compact_field(col_u, "ID User", "ID User...")
        self.entry_user.insert(0, str(self.user_data.get("id_user", "")))
        if self.role != "admin":
            self.entry_user.configure(state="disabled")

        col_l = ctk.CTkFrame(row1, fg_color="transparent")
        col_l.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        self.entry_lapangan = self._add_compact_field(col_l, "ID Lapangan", "Contoh: 1")

        self.entry_tanggal = self._add_field(
            form_card, "Tanggal (YYYY-MM-DD)", "2026-11-18"
        )

        row3 = ctk.CTkFrame(form_card, fg_color="transparent")
        row3.pack(fill="x", padx=12, pady=(0, 6))
        row3.grid_columnconfigure(0, weight=1)
        row3.grid_columnconfigure(1, weight=1)

        col_m = ctk.CTkFrame(row3, fg_color="transparent")
        col_m.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.entry_jam_mulai = self._add_compact_field(col_m, "Jam Mulai", "19:00:00")

        col_s = ctk.CTkFrame(row3, fg_color="transparent")
        col_s.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        self.entry_jam_selesai = self._add_compact_field(col_s, "Jam Selesai", "21:00:00")

        self.entry_total = self._add_field(
            form_card, "Total Biaya (Rp)", "100000"
        )

        if self.role == "admin":
            ctk.CTkLabel(
                form_card,
                text="Status Reservasi (Admin)",
                font=("Arial", 11, "bold"),
                text_color="#1F2937",
            ).pack(padx=12, anchor="w")
            self.combo_status = ctk.CTkOptionMenu(
                form_card,
                values=[
                    "menunggu_pembayaran",
                    "dikonfirmasi",
                    "selesai",
                    "dibatalkan",
                ],
                height=32,
                fg_color="#0F2C59",
                button_color="#1E3A8A",
                text_color="#FFFFFF",
            )
            self.combo_status.pack(fill="x", padx=12, pady=(2, 8))
        else:
            ctk.CTkLabel(
                form_card,
                text="Status Awal: menunggu_pembayaran (Otomatis)",
                font=("Arial", 11, "bold"),
                text_color="#2E7D32",
            ).pack(padx=12, pady=(4, 8), anchor="w")

        btn_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=12, pady=(4, 10))

        ctk.CTkButton(
            btn_frame,
            text="Simpan Reservasi",
            height=34,
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            text_color="#FFFFFF",
            font=("Arial", 12, "bold"),
            command=self._tambah_reservasi,
        ).pack(fill="x", pady=3)

        if self.role == "admin":
            ctk.CTkButton(
                btn_frame,
                text="Perbarui Reservasi (Admin)",
                height=34,
                fg_color="#007BFF",
                hover_color="#0056B3",
                text_color="#FFFFFF",
                font=("Arial", 12, "bold"),
                command=self._update_reservasi,
            ).pack(fill="x", pady=3)

            ctk.CTkButton(
                btn_frame,
                text="Hapus Reservasi (Admin)",
                height=34,
                fg_color="#DC3545",
                hover_color="#B02A37",
                text_color="#FFFFFF",
                font=("Arial", 12, "bold"),
                command=self._hapus_reservasi,
            ).pack(fill="x", pady=3)

        table_card = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#D1D5DB",
        )
        table_card.grid(row=0, column=1, sticky="nsew", pady=2)

        top_bar = ctk.CTkFrame(table_card, fg_color="transparent")
        top_bar.pack(fill="x", padx=16, pady=(12, 8))

        ctk.CTkLabel(
            top_bar,
            text="Daftar Jadwal & Transaksi Reservasi",
            font=("Arial", 15, "bold"),
            text_color="#0F2C59",
        ).pack(side="left")

        ctk.CTkButton(
            top_bar,
            text="Muat Ulang",
            width=100,
            height=30,
            fg_color="#0F2C59",
            hover_color="#1E3A8A",
            command=self.load_data,
        ).pack(side="right")

        cols = (
            "id_reservasi",
            "id_user",
            "id_lapangan",
            "tanggal",
            "mulai",
            "selesai",
            "total",
            "status",
        )
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings")
        headers = [
            ("id_reservasi", "ID", 45),
            ("id_user", "User", 55),
            ("id_lapangan", "Lap.", 55),
            ("tanggal", "Tanggal", 95),
            ("mulai", "Mulai", 75),
            ("selesai", "Selesai", 75),
            ("total", "Total (Rp)", 95),
            ("status", "Status", 145),
        ]
        for col_id, title, width in headers:
            self.tree.heading(col_id, text=title)
            self.tree.column(col_id, width=width, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)

    def _add_compact_field(self, parent, label_text, placeholder):
        ctk.CTkLabel(
            parent,
            text=label_text,
            font=("Arial", 11, "bold"),
            text_color="#1F2937",
        ).pack(anchor="w")
        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            height=31,
            fg_color="#F9FAFB",
            border_color="#CBD5E1",
            text_color="#111827",
        )
        entry.pack(fill="x", pady=(2, 0))
        return entry

    def _add_field(self, parent, label_text, placeholder):
        ctk.CTkLabel(
            parent,
            text=label_text,
            font=("Arial", 11, "bold"),
            text_color="#1F2937",
        ).pack(padx=12, anchor="w")
        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            height=31,
            fg_color="#F9FAFB",
            border_color="#CBD5E1",
            text_color="#111827",
        )
        entry.pack(fill="x", padx=12, pady=(2, 6))
        return entry

    def _set_entry_value(self, entry, value):
        prev_state = entry.cget("state")
        if prev_state == "disabled":
            entry.configure(state="normal")
        entry.delete(0, "end")
        if value is not None and str(value) != "":
            entry.insert(0, str(value))
        if prev_state == "disabled":
            entry.configure(state="disabled")

    def _clear_form(self):
        self.selected_id = None
        if self.role == "admin":
            self._set_entry_value(self.entry_user, "")
        else:
            self._set_entry_value(self.entry_user, self.user_data.get("id_user", ""))
        self._set_entry_value(self.entry_lapangan, "")
        self._set_entry_value(self.entry_tanggal, "")
        self._set_entry_value(self.entry_jam_mulai, "")
        self._set_entry_value(self.entry_jam_selesai, "")
        self._set_entry_value(self.entry_total, "")
        if self.role == "admin":
            self.combo_status.set("menunggu_pembayaran")

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = ReservasiController.get_all_reservasi()
        for row in rows:
            self.tree.insert(
                "",
                "end",
                values=(
                    row.get("id_reservasi"),
                    row.get("id_user"),
                    row.get("id_lapangan"),
                    row.get("tanggal_reservasi"),
                    row.get("jam_mulai"),
                    row.get("jam_selesai"),
                    row.get("total_harga"),
                    row.get("status_reservasi"),
                ),
            )

    def _on_row_select(self, _event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        self.selected_id = values[0]

        self._set_entry_value(self.entry_user, values[1])
        self._set_entry_value(self.entry_lapangan, values[2])
        self._set_entry_value(self.entry_tanggal, values[3])
        self._set_entry_value(self.entry_jam_mulai, values[4])
        self._set_entry_value(self.entry_jam_selesai, values[5])
        self._set_entry_value(self.entry_total, values[6])
        if self.role == "admin":
            self.combo_status.set(values[7])

    def _tambah_reservasi(self):
        id_user = (
            self.entry_user.get()
            if self.role == "admin"
            else str(self.user_data.get("id_user"))
        )
        ok, msg = ReservasiController.add_reservasi(
            id_user,
            self.entry_lapangan.get(),
            self.entry_tanggal.get(),
            self.entry_jam_mulai.get(),
            self.entry_jam_selesai.get(),
            self.entry_total.get(),
        )
        if ok:
            messagebox.showinfo("Berhasil", msg, parent=self)
            self._clear_form()
            self.load_data()
        else:
            messagebox.showerror("Gagal", msg, parent=self)

    def _update_reservasi(self):
        if not self.selected_id:
            messagebox.showwarning(
                "Peringatan", "Pilih baris reservasi terlebih dahulu!", parent=self
            )
            return
        ok, msg = ReservasiController.update_reservasi(
            self.selected_id,
            self.entry_user.get(),
            self.entry_lapangan.get(),
            self.entry_tanggal.get(),
            self.entry_jam_mulai.get(),
            self.entry_jam_selesai.get(),
            self.entry_total.get(),
            self.combo_status.get(),
        )
        if ok:
            messagebox.showinfo("Berhasil", msg, parent=self)
            self.load_data()
        else:
            messagebox.showerror("Gagal", msg, parent=self)

    def _hapus_reservasi(self):
        if not self.selected_id:
            messagebox.showwarning(
                "Peringatan", "Pilih baris reservasi terlebih dahulu!", parent=self
            )
            return
        if messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Hapus reservasi ID {self.selected_id} beserta pembayaran/riwayat terkait?",
            parent=self,
        ):
            ok, msg = ReservasiController.delete_reservasi(self.selected_id)
            if ok:
                messagebox.showinfo("Berhasil", msg, parent=self)
                self._clear_form()
                self.load_data()
            else:
                messagebox.showerror("Gagal", msg, parent=self)

    def _cancel_all_after(self):
        for aid in self._after_ids:
            try:
                self.after_cancel(aid)
            except Exception:
                pass
        self._after_ids.clear()

    def _handle_logout(self):
        if messagebox.askyesno(
            "Konfirmasi Logout",
            "Akhiri sesi dan kembali ke halaman Login?",
            parent=self,
        ):
            self.logout_requested = True
            self._cancel_all_after()
            self.quit()

    def _on_close(self):
        self.logout_requested = False
        self._cancel_all_after()
        try:
            self.quit()
        except tk.TclError:
            pass