import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter.font as tkfont
from tkinter import messagebox
import requests
import threading
import time
from app_token import get_token, get_user

class JoinGamePage(ttkb.Frame):
    def __init__(self, master, show_main_menu_callback, start_actual_game_callback):
        super().__init__(master)
        self.master = master
        self.show_main_menu_callback = show_main_menu_callback
        self.start_actual_game_callback = start_actual_game_callback

        self.games_listbox = None
        self.refresh_button = None
        self.waiting_frame = None
        self.polling = False

        self.build_ui()
        self.refresh_games()

    def build_ui(self):
        # پاک کردن همه ویجت‌های قبلی
        for widget in self.winfo_children():
            widget.destroy()

        container = ttkb.Frame(self, padding=30)
        container.place(relx=0.5, rely=0.5, anchor="center")

        # تنظیم استایل و فونت‌ها
        style = ttkb.Style()
        my_button_font_bold = tkfont.Font(family="B Nazanin", size=14, weight="bold")
        my_button_font_regular = tkfont.Font(family="B Nazanin", size=12)
        my_label_font = tkfont.Font(family="B Nazanin", size=26, weight="bold")
        style.configure("MyBold.TButton", font=my_button_font_bold)
        style.configure("MyRegular.TButton", font=my_button_font_regular)

        # عنوان صفحه
        ttkb.Label(
            container,
            text="🎮 لیست بازی‌های منتظر",
            font=my_label_font,
            bootstyle="primary"
        ).pack(pady=(0, 30))

        # لیست بازی‌ها
        self.games_listbox = ttkb.Treeview(
            container,
            columns=('creator', 'difficulty', 'created'),
            show='headings',
            height=9,
            bootstyle="info"
        )
        self.games_listbox.heading('creator', text='سازنده')
        self.games_listbox.heading('difficulty', text='سختی')
        self.games_listbox.heading('created', text='تاریخ ایجاد')
        self.games_listbox.column('creator', width=150, anchor='center')
        self.games_listbox.column('difficulty', width=120, anchor='center')
        self.games_listbox.column('created', width=140, anchor='center')
        self.games_listbox.pack(pady=15, fill='x')

        # دکمه پیوستن به بازی
        ttkb.Button(
            container,
            text="▶️ پیوستن به بازی انتخاب‌شده",
            bootstyle="success",
            width=35,
            style="MyBold.TButton",
            command=self.join_selected_game
        ).pack(pady=(20, 12))

        # دکمه بروزرسانی لیست
        self.refresh_button = ttkb.Button(
            container,
            text="🔄 بروزرسانی لیست بازی‌ها",
            bootstyle="secondary",
            width=35,
            style="MyRegular.TButton",
            command=self.refresh_games
        )
        self.refresh_button.pack(pady=8)

        # دکمه بازگشت به منو
        ttkb.Button(
            container,
            text="↩️ بازگشت به منو",
            bootstyle="danger",
            width=35,
            style="MyRegular.TButton",
            command=self.show_main_menu_callback
        ).pack(pady=(20, 0))

    def refresh_games(self):
        self.games_listbox.delete(*self.games_listbox.get_children())
        token = get_token()
        current_user = get_user()
        headers = {'Authorization': f'Bearer {token}'}
        try:
            r = requests.get("http://127.0.0.1:8000/api/waiting-games/", headers=headers)
            if r.status_code == 200:
                for g in r.json():
                    if g['player1'] == current_user:
                        continue
                    self.games_listbox.insert(
                        '',
                        'end',
                        iid=g['id'],
                        values=(
                            g['player1'],
                            {'easy': 'آسان', 'medium': 'متوسط', 'hard': 'سخت'}.get(g['difficulty'], g['difficulty']),
                            g['created_at'].split('T')[0]
                        )
                    )
            else:
                messagebox.showerror("خطا", "عدم دریافت لیست بازی‌ها.")
        except Exception as e:
            messagebox.showerror("خطا", str(e))

    def join_selected_game(self):
        selection = self.games_listbox.selection()
        if not selection:
            messagebox.showwarning("تذکر", "لطفاً یک بازی را انتخاب کنید.")
            return

        game_id = selection[0]
        token = get_token()
        headers = {'Authorization': f'Bearer {token}'}
        try:
            r = requests.post(f"http://127.0.0.1:8000/api/games/{game_id}/join/", headers=headers)
            if r.status_code == 200:
                self.show_waiting_for_start(game_id)
            else:
                err = r.json().get('error', 'خطا در پیوستن به بازی.')
                if "your own game" in err:
                    messagebox.showwarning("تذکر", "نمی‌توانید به بازی‌ای که خودتان ساخته‌اید بپیوندید.")
                elif "two players" in err:
                    messagebox.showwarning("تذکر", "این بازی قبلاً شروع شده است.")
                elif "cannot join this game" in err:
                    messagebox.showwarning("تذکر", "این بازی دیگر قابل پیوستن نیست.")
                else:
                    messagebox.showerror("خطا", err)
                self.refresh_games()
        except Exception as e:
            messagebox.showerror("خطا", str(e))

    def show_waiting_for_start(self, game_id):
        for widget in self.winfo_children():
            widget.destroy()
        self.waiting_frame = ttkb.Frame(self, padding=30)
        self.waiting_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttkb.Label(
            self.waiting_frame,
            text="⏳ در حال آماده‌سازی بازی...",
            font=("B Nazanin", 20),
            bootstyle="info"
        ).pack(pady=(0, 30))

        ttkb.Button(
            self.waiting_frame,
            text="↩️ بازگشت به منو",
            bootstyle="danger",
            width=25,
            command=self.cancel_and_return
        ).pack()

        self.polling = True
        threading.Thread(target=self.poll_game_status, args=(game_id,), daemon=True).start()

    def poll_game_status(self, game_id):
        token = get_token()
        headers = {'Authorization': f'Bearer {token}'}
        while self.polling:
            try:
                r = requests.get(f"http://127.0.0.1:8000/api/games/{game_id}/status/", headers=headers)
                if r.status_code == 200:
                    status = r.json().get('status')
                    if status == 'active':
                        self.polling = False
                        self.master.after(0, lambda: self.start_actual_game_callback(game_id))
                        return
                time.sleep(2)
            except Exception:
                time.sleep(2)

    def cancel_and_return(self):
        self.polling = False
        self.show_main_menu_callback()
