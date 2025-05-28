import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import messagebox
import requests
from app_token import set_tokens, set_user

API_URL = "http://127.0.0.1:8000/api/login/"

class LoginPage(ttkb.Frame):
    def __init__(self, master, show_register_callback, show_after_login_callback):
        super().__init__(master)
        self.show_register_callback = show_register_callback
        self.show_after_login_callback = show_after_login_callback

        container = ttkb.Frame(self, padding=30)
        container.place(relx=0.5, rely=0.5, anchor="center")

        ttkb.Label(
            container,
            text="🔐 ورود به حساب کاربری",
            font=("B Nazanin", 24, "bold"),
            bootstyle="info"
        ).pack(pady=(0, 25))

        self.username_var = ttkb.StringVar()
        self.password_var = ttkb.StringVar()

        ttkb.Label(container, text="نام کاربری:", font=("B Nazanin", 14)).pack(anchor="w", padx=10)
        ttkb.Entry(container, textvariable=self.username_var, font=("B Nazanin", 13), width=30).pack(pady=7)

        ttkb.Label(container, text="رمز عبور:", font=("B Nazanin", 14)).pack(anchor="w", padx=10)
        ttkb.Entry(container, textvariable=self.password_var, font=("B Nazanin", 13), show="*", width=30).pack(pady=7)

        btn_opts = dict(width=28, padding=10)

        ttkb.Button(
            container,
            text="🚪 ورود",
            bootstyle="info-outline",
            command=self.login,
            **btn_opts
        ).pack(pady=16)

        ttkb.Button(
            container,
            text="📝 ثبت‌نام",
            bootstyle="secondary-outline",
            command=self.show_register_callback,
            **btn_opts
        ).pack()

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            messagebox.showwarning("خطا", "همه فیلدها باید پر شوند.")
            return

        try:
            response = requests.post(API_URL, json={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                data = response.json()
                set_tokens(data['access'], data.get('refresh'))
                set_user(username)
                messagebox.showinfo("خوش آمدید", f"{username} عزیز، خوش آمدید! 🎉")
                self.show_after_login_callback()
            else:
                try:
                    msg = response.json().get("detail") or response.json().get("message") or "ورود ناموفق بود."
                except Exception:
                    msg = "ورود ناموفق بود."
                messagebox.showerror("خطا", msg)
        except Exception as e:
            messagebox.showerror("خطا", "ارتباط با سرور برقرار نشد.\n" + str(e))
