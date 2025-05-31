# profile_page.py
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import messagebox
import requests
from app_token import get_token, clear_auth

API_PROFILE_URL = "http://127.0.0.1:8000/api/profile/"
API_PROFILE_EDIT_URL = "http://127.0.0.1:8000/api/profile/edit/"


class ProfilePage(ttkb.Frame):
    def __init__(self, master, show_menu_callback, show_logout_callback):
        super().__init__(master)
        self.show_menu_callback = show_menu_callback
        self.show_logout_callback = show_logout_callback

        # === Layout ===
        container = ttkb.Frame(self)
        container.place(relx=0.5, rely=0.1, anchor="n")

        ttkb.Label(container, text="پروفایل کاربر", font=("B Nazanin", 26, "bold"), bootstyle="primary").pack(pady=20)

        # ==== User Info Section ====
        user_info_frame = ttkb.LabelFrame(container, text="👤 اطلاعات کاربری", bootstyle="light")
        user_info_frame.pack(fill="x", padx=10, pady=10)

        ttkb.Label(user_info_frame, text="نام کاربری:", font=("B Nazanin", 14)).pack(anchor="w", pady=2)
        self.username_entry = ttkb.Entry(user_info_frame, font=("B Nazanin", 14))
        self.username_entry.pack(fill="x", pady=2)

        self.score_label = ttkb.Label(user_info_frame, font=("B Nazanin", 14))
        self.score_label.pack(anchor="w", pady=3)

        self.rank_label = ttkb.Label(user_info_frame, font=("B Nazanin", 14), bootstyle="warning")
        self.rank_label.pack(anchor="w", pady=3)

        # ==== Game Stats Section ====
        stats_frame = ttkb.LabelFrame(container, text="📊 آمار بازی‌ها", bootstyle="info")
        stats_frame.pack(fill="x", padx=10, pady=10)

        self.games_played_label = ttkb.Label(stats_frame, font=("B Nazanin", 13))
        self.games_played_label.pack(anchor="w", pady=2)

        self.wins_label = ttkb.Label(stats_frame, font=("B Nazanin", 13), bootstyle="success")
        self.wins_label.pack(anchor="w", pady=2)

        self.losses_label = ttkb.Label(stats_frame, font=("B Nazanin", 13), bootstyle="danger")
        self.losses_label.pack(anchor="w", pady=2)

        self.win_rate_label = ttkb.Label(stats_frame, font=("B Nazanin", 13), bootstyle="secondary")
        self.win_rate_label.pack(anchor="w", pady=2)

        # ==== Buttons ====
        button_frame = ttkb.Frame(container)
        button_frame.pack(pady=20)

        ttkb.Button(button_frame, text="ذخیره تغییرات", bootstyle="success", width=20, command=self.save_profile).pack(side="left", padx=10)
        ttkb.Button(button_frame, text="بازگشت به منو", bootstyle="primary", width=20, command=self.show_menu_callback).pack(side="left", padx=10)
        ttkb.Button(button_frame, text="خروج از حساب", bootstyle="danger", width=20, command=self.logout).pack(side="left", padx=10)

        self.load_profile()

    def load_profile(self):
        token = get_token()
        if not token:
            messagebox.showerror("خطا", "ابتدا وارد شوید.")
            return

        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(API_PROFILE_URL, headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.username_entry.delete(0, "end")
                self.username_entry.insert(0, data.get('username', ''))

                self.score_label.config(text=f"امتیاز: {data.get('score', 0)}")
                self.rank_label.config(text=f"رتبه در جدول: {data.get('rank', 'نامشخص')}")

                self.games_played_label.config(text=f"تعداد بازی‌ها: {data.get('games_played', 0)}")
                self.wins_label.config(text=f"بردها: {data.get('wins', 0)}")
                self.losses_label.config(text=f"باخت‌ها: {data.get('losses', 0)}")
                self.win_rate_label.config(text=f"درصد برد: {data.get('win_rate', '0%')}")
            else:
                msg = response.json().get("detail") or "خطا در دریافت اطلاعات پروفایل."
                messagebox.showerror("خطا", msg)
        except Exception as e:
            messagebox.showerror("خطا", "ارتباط با سرور برقرار نشد.\n" + str(e))

    def save_profile(self):
        token = get_token()
        if not token:
            messagebox.showerror("خطا", "ابتدا وارد شوید.")
            return

        new_username = self.username_entry.get().strip()
        if not new_username:
            messagebox.showerror("خطا", "نام کاربری نمی‌تواند خالی باشد.")
            return

        try:
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            payload = {"username": new_username}
            response = requests.put(API_PROFILE_EDIT_URL, json=payload, headers=headers)
            if response.status_code == 200:
                messagebox.showinfo("موفقیت", "پروفایل با موفقیت به‌روزرسانی شد.")
                self.load_profile()  # بروز رسانی اطلاعات بعد از ویرایش
            else:
                err_msg = response.json().get("username") or response.json().get("detail") or "خطا در به‌روزرسانی پروفایل."
                messagebox.showerror("خطا", err_msg)
        except Exception as e:
            messagebox.showerror("خطا", "ارتباط با سرور برقرار نشد.\n" + str(e))

    def logout(self):
        clear_auth()
        self.show_logout_callback()


