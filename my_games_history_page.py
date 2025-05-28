import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import messagebox
import requests
from app_token import get_token
from datetime import datetime

HISTORY_URL = "http://127.0.0.1:8000/api/history/"


class MyGamesHistoryPage(ttkb.Frame):
    def __init__(self, master, show_menu_callback):
        super().__init__(master)
        self.show_menu_callback = show_menu_callback

        container = ttkb.Frame(self)
        container.pack(fill="both", expand=True, pady=15, padx=15)

        ttkb.Label(
            container,
            text="📜 تاریخچه بازی‌های من",
            font=("B Nazanin", 22, "bold"),
            bootstyle="warning"
        ).pack(pady=10)

        ttkb.Button(
            container,
            text="🔙 بازگشت به منو",
            bootstyle="secondary",
            width=16,
            command=self.show_menu_callback
        ).pack(pady=5)

        # ایجاد فریم برای جدول
        table_frame = ttkb.Frame(container)
        table_frame.pack(fill="both", expand=True, pady=10)

        # ایجاد ستون‌های جدول
        columns = ("id", "opponent", "difficulty", "started_at", "result")

        self.tree = ttkb.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            bootstyle="secondary",
            height=15
        )

        # تنظیم عنوان ستون‌ها
        self.tree.heading("id", text="🆔 شناسه بازی")
        self.tree.heading("opponent", text="👤 حریف")
        self.tree.heading("difficulty", text="🎚 سطح")
        self.tree.heading("started_at", text="🕒 تاریخ شروع")
        self.tree.heading("result", text="🎯 نتیجه")

        # تنظیم عرض ستون‌ها
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("opponent", width=150, anchor="center")
        self.tree.column("difficulty", width=100, anchor="center")
        self.tree.column("started_at", width=150, anchor="center")
        self.tree.column("result", width=100, anchor="center")

        # اضافه کردن جدول به فریم و اسکرول بار عمودی
        scrollbar = ttkb.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.load_history()

    def load_history(self):
        # خالی کردن جدول قبلی
        for row in self.tree.get_children():
            self.tree.delete(row)

        token = get_token()
        if not token:
            messagebox.showerror("خطا", "ابتدا وارد شوید.")
            return

        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(HISTORY_URL, headers=headers)
            if response.status_code == 200:
                games = response.json()

                if not games:
                    messagebox.showinfo("اطلاع", "هیچ بازی به پایان نرسیده 😕")
                else:
                    for game in games:
                        self.insert_game_row(game)
            else:
                msg = response.json().get("detail", "خطا در دریافت اطلاعات.")
                messagebox.showerror("خطا", msg)
        except Exception as e:
            messagebox.showerror("خطا", str(e))

    def insert_game_row(self, game):
        opponent = game.get("opponent", "-")
        difficulty = self._fa_difficulty(game.get("difficulty", ""))
        started_at = self._persian_time(game.get("started_at"))
        result = game.get("result", None)

        # تعیین متن و رنگ نتیجه
        if result == "win":
            result_text = "🏆 برد"
            tag = "win"
        elif result == "lose":
            result_text = "❌ باخت"
            tag = "lose"
        elif result == "draw":
            result_text = "🤝 مساوی"
            tag = "draw"
        else:
            result_text = "❓ نامشخص"
            tag = "unknown"

        self.tree.insert(
            "",
            "end",
            values=(game["id"], opponent, difficulty, started_at, result_text),
            tags=(tag,)
        )

        # تعریف رنگ‌ها برای تگ‌ها
        self.tree.tag_configure("win", background="#d4edda", foreground="#155724")  # سبز روشن
        self.tree.tag_configure("lose", background="#f8d7da", foreground="#721c24")  # قرمز روشن
        self.tree.tag_configure("draw", background="#fff3cd", foreground="#856404")  # زرد روشن
        self.tree.tag_configure("unknown", background="#e2e3e5", foreground="#6c757d")  # خاکستری

    def _fa_difficulty(self, difficulty):
        return {
            "easy": "ساده",
            "medium": "متوسط",
            "hard": "سخت"
        }.get(difficulty, "نامشخص")

    def _persian_time(self, iso_str):
        try:
            dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
            return dt.strftime("%Y/%m/%d %H:%M")
        except Exception:
            return iso_str
