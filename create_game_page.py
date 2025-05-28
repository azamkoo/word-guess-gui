import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import requests
import threading
import time
from tkinter import messagebox

from app_token import get_token


class CreateGamePage(ttkb.Frame):
    def __init__(self, master, show_main_menu_callback):
        super().__init__(master)
        self.master = master
        self.show_main_menu_callback = show_main_menu_callback
        self.polling = False

        container = ttkb.Frame(self, padding=20)
        container.place(relx=0.5, rely=0.5, anchor="center")

        ttkb.Label(
            container,
            text="🎯 انتخاب سختی بازی",
            font=("B Nazanin", 22, "bold"),
            bootstyle="primary"
        ).pack(pady=(0, 25))

        self.difficulty_var = ttkb.StringVar(value='easy')
        for diff, label in [('easy', 'آسان'), ('medium', 'متوسط'), ('hard', 'سخت')]:
            ttkb.Radiobutton(
                container,
                text=label,
                variable=self.difficulty_var,
                value=diff,
                bootstyle="primary"
            ).pack(anchor='w', padx=20, pady=4)

        ttkb.Button(
            container,
            text="🚀 ایجاد بازی",
            width=25,
            bootstyle="success",
            command=self.create_game
        ).pack(pady=(25, 10))

        ttkb.Button(
            container,
            text="↩️ بازگشت به منو",
            width=25,
            bootstyle="secondary",
            command=self.show_main_menu_callback
        ).pack()

    def create_game(self):
        difficulty = self.difficulty_var.get()
        token = get_token()
        headers = {'Authorization': f'Bearer {token}'}
        data = {'difficulty': difficulty}
        try:
            response = requests.post('http://127.0.0.1:8000/api/create-game/', json=data, headers=headers)
            if response.status_code == 201:
                game_info = response.json()
                self.show_waiting_for_opponent(game_info)
            else:
                messagebox.showerror("خطا", f"خطا در ایجاد بازی: {response.json()}")
        except Exception as e:
            messagebox.showerror("خطا", str(e))

    def show_waiting_for_opponent(self, game_info):
        # پاک کردن همه ویجت‌ها
        for widget in self.winfo_children():
            widget.destroy()

        waiting_frame = ttkb.Frame(self, padding=30)
        waiting_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttkb.Label(
            waiting_frame,
            text="⏳ در انتظار پیوستن بازیکن دیگر...",
            font=("B Nazanin", 20),
            bootstyle="info"
        ).pack(pady=(0, 20))

        ttkb.Label(
            waiting_frame,
            text=f"🎲 سختی: {game_info['difficulty']}  |  طول کلمه: {game_info['word_length']}",
            font=("B Nazanin", 16)
        ).pack(pady=(0, 25))

        ttkb.Button(
            waiting_frame,
            text="❌ لغو و بازگشت به منو",
            width=25,
            bootstyle="danger",
            command=lambda: self.leave_game(game_info['game_id'])
        ).pack()

        self.polling = True
        threading.Thread(target=self.poll_game_status, args=(game_info['game_id'],), daemon=True).start()

    def poll_game_status(self, game_id):
        while self.polling:
            token = get_token()
            headers = {'Authorization': f'Bearer {token}'}
            try:
                response = requests.get(f'http://127.0.0.1:8000/api/games/{game_id}/status/', headers=headers)
                if response.status_code == 200:
                    status = response.json().get('status')
                    if status == 'active':
                        self.polling = False
                        self.master.after(0, lambda: self.master.start_actual_game(game_id))
                        return
                time.sleep(2.5)
            except Exception:
                time.sleep(2.5)

    def leave_game(self, game_id):
        self.polling = False
        token = get_token()
        headers = {'Authorization': f'Bearer {token}'}
        try:
            requests.post(f'http://127.0.0.1:8000/api/games/{game_id}/cancel/', headers=headers)
        except Exception:
            pass
        self.show_main_menu_callback()
