# profile_page.py
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import messagebox
import requests
from app_token import get_token, get_user

API_URL = "http://127.0.0.1:8000/api/profile/"

class ProfilePage(ttkb.Frame):
    def __init__(self, master, show_menu_callback, show_logout_callback):
        super().__init__(master)
        self.show_menu_callback = show_menu_callback
        self.show_logout_callback = show_logout_callback

        container = ttkb.Frame(self)
        container.place(relx=0.5, rely=0.25, anchor="n")

        ttkb.Label(container, text="پروفایل کاربر", font=("B Nazanin", 24, "bold"), bootstyle="primary").pack(pady=20)

        self.username_label = ttkb.Label(container, font=("B Nazanin", 16))
        self.username_label.pack(pady=5)

        self.score_label = ttkb.Label(container, font=("B Nazanin", 14), bootstyle="success")
        self.score_label.pack(pady=5)

        stats_frame = ttkb.LabelFrame(container, text="آمار بازی‌ها", bootstyle="info")
        stats_frame.pack(fill="x", pady=15, ipadx=10, ipady=5)

        self.games_played_label = ttkb.Label(stats_frame, font=("B Nazanin", 13))
        self.games_played_label.pack(anchor="w", pady=2)

        self.wins_label = ttkb.Label(stats_frame, font=("B Nazanin", 13))
        self.wins_label.pack(anchor="w", pady=2)

        self.losses_label = ttkb.Label(stats_frame, font=("B Nazanin", 13))
        self.losses_label.pack(anchor="w", pady=2)

        self.win_rate_label = ttkb.Label(stats_frame, font=("B Nazanin", 13))
        self.win_rate_label.pack(anchor="w", pady=2)

        # ==== New Menu Button ====
        ttkb.Button(container, text="منو", bootstyle="info", width=20, command=self.show_menu_callback).pack(pady=10)

        ttkb.Button(container, text="خروج از حساب", bootstyle="danger", command=self.logout).pack(pady=10)

        self.load_profile()

    def load_profile(self):
        token = get_token()
        if not token:
            messagebox.showerror("خطا", "ابتدا وارد شوید.")
            return
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(API_URL, headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.username_label.config(text=f"👤 {data['username']}")
                self.score_label.config(text=f"امتیاز: {data['score']}")
                self.games_played_label.config(text=f"تعداد بازی‌ها: {data['games_played']}")
                self.wins_label.config(text=f"بردها: {data['wins']}")
                self.losses_label.config(text=f"باخت‌ها: {data['losses']}")
                self.win_rate_label.config(text=f"درصد برد: {data['win_rate']}")
            else:
                msg = response.json().get("detail") or "خطا در دریافت اطلاعات پروفایل."
                messagebox.showerror("خطا", msg)
        except Exception as e:
            messagebox.showerror("خطا", "ارتباط با سرور برقرار نشد.\n" + str(e))

    def logout(self):
        from app_token import clear_auth
        clear_auth()
        self.show_logout_callback()
