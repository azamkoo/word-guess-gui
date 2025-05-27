# my_games_history_page.py
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import messagebox
import requests
from app_token import get_token
from datetime import datetime

API_URL = "http://127.0.0.1:8000/api/profile/"

class MyGamesHistoryPage(ttkb.Frame):
    def __init__(self, master, show_menu_callback):
        super().__init__(master)
        self.show_menu_callback = show_menu_callback

        # Vertical stacking
        container = ttkb.Frame(self)
        container.pack(fill="x", pady=15)

        ttkb.Label(
            container, text="تاریخچه بازی‌های من",
            font=("B Nazanin", 22, "bold"),
            bootstyle="warning"
        ).pack(pady=10)

        ttkb.Button(
            container, text="بازگشت به منو",
            bootstyle="secondary",
            width=16,
            command=self.show_menu_callback
        ).pack(pady=5)

        # Game list frame
        self.list_frame = ttkb.Frame(self)
        self.list_frame.pack(fill="both", expand=True, pady=15)

        self.load_history()

    def load_history(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        token = get_token()
        if not token:
            messagebox.showerror("خطا", "ابتدا وارد شوید.")
            return
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(API_URL, headers=headers)
            if response.status_code == 200:
                data = response.json()
                finished_games = data.get("finished_games", [])
                username = data.get("username", "")

                if not finished_games:
                    ttkb.Label(self.list_frame, text="هیچ بازی به پایان نرسیده.", font=("B Nazanin", 14)).pack(pady=15)
                else:
                    for g in finished_games:
                        self.add_game_row(g, username)
            else:
                msg = response.json().get("error") or response.json().get("detail") or "خطا در دریافت اطلاعات."
                messagebox.showerror("خطا", msg)
        except Exception as e:
            messagebox.showerror("خطا", str(e))

    def add_game_row(self, game, current_username):
        frame = ttkb.Frame(self.list_frame)
        frame.pack(fill="x", padx=8, pady=7)

        # Find opponent name
        player1 = game.get("player1")
        player2 = game.get("player2")
        opponent = player2 if player1 == current_username else player1

        # Detect result
        result = game.get("result")
        result_fa = "نامشخص"
        color = ""
        if result == "win":
            if game.get("turn") == current_username:
                result_fa = "برد"
                color = "success"
            else:
                result_fa = "باخت"
                color = "danger"
        elif result == "lose":
            result_fa = "باخت"
            color = "danger"
        else:
            result_fa = "نامشخص"
            color = "secondary"

        info = (
            f"🆔 {game['id']}   "
            f"👤 حریف: {opponent or '-'}   "
            f"🎚 سطح: {self._fa_difficulty(game['difficulty'])}   "
            f"🕒 {self._persian_time(game.get('started_at'))}"
        )
        ttkb.Label(frame, text=info, font=("B Nazanin", 13)).pack(side="left", padx=5)

        ttkb.Label(
            frame,
            text=f"{result_fa}",
            font=("B Nazanin", 12, "bold"),
            bootstyle=color
        ).pack(side="right", padx=8)

    def _fa_difficulty(self, difficulty):
        return {"easy": "ساده", "medium": "متوسط", "hard": "سخت"}.get(difficulty, difficulty)

    def _persian_time(self, iso_str):
        try:
            dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
            return dt.strftime("%Y/%m/%d %H:%M")
        except Exception:
            return iso_str
