# register_page.py
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8000/api/register/"

class RegisterPage(ttkb.Frame):
    def __init__(self, master, show_login_callback):
        super().__init__(master)
        self.show_login_callback = show_login_callback

        container = ttkb.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        ttkb.Label(container, text="ثبت‌نام", font=("B Nazanin", 24, "bold"), bootstyle="success").pack(pady=20)

        self.username_var = ttkb.StringVar()
        self.password_var = ttkb.StringVar()

        ttkb.Label(container, text="نام کاربری:", font=("B Nazanin", 14)).pack(anchor="w", padx=10)
        ttkb.Entry(container, textvariable=self.username_var, font=("B Nazanin", 13), width=30).pack(pady=7)

        ttkb.Label(container, text="رمز عبور:", font=("B Nazanin", 14)).pack(anchor="w", padx=10)
        ttkb.Entry(container, textvariable=self.password_var, font=("B Nazanin", 13), show="*", width=30).pack(pady=7)

        ttkb.Button(container, text="ثبت‌نام", bootstyle="success", width=25, command=self.register).pack(pady=16)
        ttkb.Button(container, text="بازگشت به ورود", bootstyle="secondary", width=25, command=self.show_login_callback).pack()

    def register(self):
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
            if response.status_code == 201:
                messagebox.showinfo("تبریک!", "ثبت‌نام با موفقیت انجام شد! حالا وارد شوید.")
                self.show_login_callback()
            else:
                msg = response.json().get("error", "ثبت‌نام ناموفق بود.")

                messagebox.showerror("خطا", msg)
        except Exception as e:
            messagebox.showerror("خطا", "ارتباط با سرور برقرار نشد.\n" + str(e))
