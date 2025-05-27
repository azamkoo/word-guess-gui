# main_menu_page.py
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *


class MainMenuPage(ttkb.Frame):
    def __init__(self, master, create_game_callback, join_game_callback, show_history_callback, show_profile_callback,
                 logout_callback):
        super().__init__(master)
        self.master = master

        container = ttkb.Frame(self)
        container.place(relx=0.5, rely=0.4, anchor="center")

        ttkb.Label(container, text="منوی اصلی", font=("B Nazanin", 28, "bold"), bootstyle="primary").pack(pady=30)

        ttkb.Button(
            container,
            text="ایجاد بازی جدید",
            bootstyle="success",
            width=30,
            command=create_game_callback
        ).pack(pady=15)

        ttkb.Button(
            container,
            text="پیوستن به بازی",
            bootstyle="info",
            width=30,
            command=join_game_callback
        ).pack(pady=15)

        ttkb.Button(
            container,
            text="تاریخچه بازی‌های من",
            bootstyle="warning",
            width=30,
            command=show_history_callback
        ).pack(pady=15)

        ttkb.Button(
            container,
            text="بازگشت به پروفایل",
            bootstyle="primary",
            width=30,
            command=show_profile_callback
        ).pack(pady=15)

        ttkb.Button(
            container,
            text="خروج از حساب",
            bootstyle="danger",
            width=30,
            command=logout_callback
        ).pack(pady=25)
