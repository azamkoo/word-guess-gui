import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

class StartPage(ttkb.Frame):
    def __init__(self, master, show_register_callback, show_login_callback, exit_callback):
        super().__init__(master)
        self.master = master

        # Central container for beauty
        container = ttkb.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ttkb.Label(
            container,
            text="\"به بازی حدس کلمات کیوووراوند خوش آمدید\"",
            font=("B Nazanin", 26, "bold"),
            bootstyle="primary"
        ).pack(pady=30)

        # Register button
        ttkb.Button(
            container,
            text="ثبت‌نام",
            width=25,
            bootstyle="success",
            command=show_register_callback
        ).pack(pady=15)

        # Login button
        ttkb.Button(
            container,
            text="ورود",
            width=25,
            bootstyle="info",
            command=show_login_callback
        ).pack(pady=15)

        # Exit button
        ttkb.Button(
            container,
            text="خروج",
            width=25,
            bootstyle="danger",
            command=exit_callback
        ).pack(pady=15)
