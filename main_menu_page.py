import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

class MainMenuPage(ttkb.Frame):
    def __init__(self, master, create_game_callback, join_game_callback, show_history_callback, show_profile_callback,
                 logout_callback, show_leaderboard_callback):
        super().__init__(master)
        self.master = master

        container = ttkb.Frame(self, padding=30)
        container.place(relx=0.5, rely=0.4, anchor="center")

        ttkb.Label(
            container,
            text="🎮 منوی اصلی بازی",
            font=("B Nazanin", 28, "bold"),
            bootstyle="primary"
        ).pack(pady=(0, 30))

        btn_opts = dict(width=32, padding=10)

        ttkb.Button(
            container,
            text="➕ ایجاد بازی جدید",
            bootstyle="success-outline",
            command=create_game_callback,
            **btn_opts
        ).pack(pady=8)

        ttkb.Button(
            container,
            text="🔗 پیوستن به بازی",
            bootstyle="info-outline",
            command=join_game_callback,
            **btn_opts
        ).pack(pady=8)

        ttkb.Button(
            container,
            text="📜 تاریخچه بازی‌های من",
            bootstyle="warning-outline",
            command=show_history_callback,
            **btn_opts
        ).pack(pady=8)

        ttkb.Button(
            container,
            text="🏆 لیست برترین‌ها",
            bootstyle="info-outline",
            command=show_leaderboard_callback,
            **btn_opts
        ).pack(pady=8)

        ttkb.Button(
            container,
            text="👤 بازگشت به پروفایل",
            bootstyle="primary-outline",
            command=show_profile_callback,
            **btn_opts
        ).pack(pady=8)

        ttkb.Button(
            container,
            text="🚪 خروج از حساب",
            bootstyle="danger-outline",
            command=logout_callback,
            **btn_opts
        ).pack(pady=(20, 0))
