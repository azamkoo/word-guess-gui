import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

class StartPage(ttkb.Frame):
    def __init__(self, master, show_register_callback, show_login_callback, exit_callback):
        super().__init__(master)
        self.master = master

        container = ttkb.Frame(self, padding=30)  # بدون bootstyle (بدون رنگ پس‌زمینه)
        container.place(relx=0.5, rely=0.5, anchor="center")

        title_lbl = ttkb.Label(
            container,
            text="🎮 بازی حدس کلمات خوش آمدید! 🎉",
            font=("B Nazanin", 28, "bold"),
            bootstyle="primary"
        )
        title_lbl.pack(pady=(0, 40))

        btn_opts = dict(width=28, padding=10)

        ttkb.Button(
            container,
            text="📝 ثبت‌نام",
            command=show_register_callback,
            bootstyle="success-outline",
            **btn_opts
        ).pack(pady=12)

        ttkb.Button(
            container,
            text="🔑 ورود",
            command=show_login_callback,
            bootstyle="info-outline",
            **btn_opts
        ).pack(pady=12)

        ttkb.Button(
            container,
            text="🚪 خروج",
            command=exit_callback,
            bootstyle="danger-outline",
            **btn_opts
        ).pack(pady=12)
