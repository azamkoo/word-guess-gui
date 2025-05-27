import ttkbootstrap as ttkb
from tkinter import messagebox
import requests
from app_token import get_token

class ActualGamePage(ttkb.Frame):
    def __init__(self, master, game_id, player1, player2, word_length, turn_username, show_main_menu_callback):
        super().__init__(master)
        self.master = master
        self.game_id = game_id
        self.player1 = player1
        self.player2 = player2
        self.word_length = word_length
        self.game_status = "active"
        self.turn_username = turn_username
        self.show_main_menu_callback = show_main_menu_callback
        self.masked_word = "_" * word_length
        self.your_username = getattr(master, 'username', None) or ""
        self.your_score = 0
        self.game_finished = False  # برای جلوگیری از چند بار نمایش پیام پایان بازی

        self.build_ui()

        # شروع polling وضعیت بازی
        self.poll_game_status()

    def build_ui(self):
        ttkb.Label(self, text="بازی حدس کلمه", font=("B Nazanin", 24, "bold"), bootstyle="info").pack(pady=15)

        self.lbl_masked_word = ttkb.Label(self, text=' '.join(self.masked_word.upper()), font=("B Nazanin", 36))
        self.lbl_masked_word.pack(pady=20)

        self.lbl_turn = ttkb.Label(self, text=f"نوبت: {self.turn_username}", font=("B Nazanin", 16))
        self.lbl_turn.pack(pady=5)

        self.lbl_score = ttkb.Label(self, text=f"امتیاز شما: {self.your_score}", font=("B Nazanin", 16))
        self.lbl_score.pack(pady=5)

        frm = ttkb.Frame(self)
        frm.pack(pady=10)

        ttkb.Label(frm, text="حرف را وارد کنید:", font=("B Nazanin", 14)).pack(side="left", padx=5)
        self.letter_var = ttkb.StringVar()
        self.entry_letter = ttkb.Entry(frm, textvariable=self.letter_var, width=3, font=("B Nazanin", 18))
        self.entry_letter.pack(side="left")

        self.btn_guess = ttkb.Button(frm, text="حدس بزن", bootstyle="success", command=self.send_guess)
        self.btn_guess.pack(side="left", padx=10)

        self.lbl_msg = ttkb.Label(self, text="", font=("B Nazanin", 14))
        self.lbl_msg.pack(pady=10)

        
        self.btn_pause = ttkb.Button(self, text="توقف بازی", bootstyle="warning", command=self.pause_game)
        self.btn_pause.pack(pady=5)
        self.btn_resume = ttkb.Button(self, text="ادامه بازی", bootstyle="primary", command=self.resume_game)
        self.btn_resume.pack(pady=5)
        self.lbl_msg = ttkb.Label(self, text="", font=("B Nazanin", 14))
        self.lbl_msg.pack(pady=10)
        ttkb.Button(self, text="بازگشت به منو", bootstyle="danger", command=self.show_main_menu_callback).pack(pady=10)
         # اول دکمه ادامه رو غیرفعال کن چون بازی اول فعال است
        self.btn_resume.configure(state="disabled")



    def send_guess(self):
        if self.game_finished:
            return  # اگر بازی تموم شده اجازه حدس نده

        letter = self.letter_var.get().strip().lower()
        if len(letter) != 1 or not letter.isalpha():
            messagebox.showwarning("هشدار", "لطفاً یک حرف معتبر وارد کنید.")
            return

        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"http://127.0.0.1:8000/api/games/{self.game_id}/guess/"

        try:
            response = requests.post(url, json={"letter": letter}, headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.masked_word = data.get("masked_word", self.masked_word)
                self.turn_username = data.get("next_turn", self.turn_username)
                self.your_score = data.get("your_score", self.your_score)
                game_status = data.get("game_status", "")

                self.update_ui()

                if data.get("correct"):
                    self.lbl_msg.configure(text="حدس درست بود!", foreground="green")
                else:
                    self.lbl_msg.configure(text="حدس نادرست بود!", foreground="red")

                if game_status == "finished":
                    self.handle_game_finished(data)
            else:
                error_msg = response.json().get("error", "خطا در ارسال حدس.")
                messagebox.showerror("خطا", error_msg)
        except Exception as e:
            messagebox.showerror("خطا", f"خطای شبکه:\n{e}")

        self.letter_var.set("")

    
    def update_ui(self):
        self.lbl_masked_word.configure(text=' '.join(self.masked_word.upper()))
        self.lbl_turn.configure(text=f"نوبت: {self.turn_username}")
        self.lbl_score.configure(text=f"امتیاز شما: {self.your_score}")

        if self.game_status == "paused":
            # وقتی بازی متوقف است، دکمه حدس و ورودی غیر فعال، دکمه ادامه فعال
            self.entry_letter.configure(state="disabled")
            self.btn_guess.configure(state="disabled")
            self.btn_pause.configure(state="disabled")
            self.btn_resume.configure(state="normal")
        else:
            # وقتی بازی فعال است همه فعال باشند
            self.entry_letter.configure(state="normal")
            self.btn_guess.configure(state="normal")
            self.btn_pause.configure(state="normal")
            self.btn_resume.configure(state="disabled")

    def handle_game_finished(self, data):
     if self.game_finished:
        return
     self.game_finished = True

     player1_score = data.get("player1_score", 0)
     player2_score = data.get("player2_score", 0)
     winner = None

     if player1_score == player2_score:
        message = "بازی مساوی شد!"
     else:
        if player1_score > player2_score:
            winner = self.player1
            loser = self.player2
        else:
            winner = self.player2
            loser = self.player1

        if self.your_username == winner:
            message = f"تبریک! شما برنده شدید 🎉"
        else:
            message = f"متاسفانه شما بازنده شدید. برنده بازی: {winner}"

     messagebox.showinfo("پایان بازی", message)
     self.show_main_menu_callback()


    def poll_game_status(self):
        if self.game_finished:
            return  # اگر بازی تموم شده polling رو قطع کن

        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"http://127.0.0.1:8000/api/games/{self.game_id}/status/"

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", "")
                turn = data.get("turn", self.turn_username)
                masked_word = data.get("masked_word", self.masked_word)
                your_score = data.get("your_score", self.your_score)
                winner = data.get("winner")

                # بروز رسانی داده ها
                self.turn_username = turn
                self.masked_word = masked_word
                self.your_score = your_score
                self.update_ui()

                if status == "finished":
                    self.handle_game_finished(data)
            # ادامه polling
            self.after(3000, self.poll_game_status)
        except Exception:
            # در صورت خطا فقط ادامه polling بده
            self.after(3000, self.poll_game_status)

    def pause_game(self):
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"http://127.0.0.1:8000/api/games/{self.game_id}/pause/"

        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                self.game_status = "paused"
                self.lbl_msg.configure(text="بازی متوقف شد.", foreground="orange")
                self.update_ui()
            else:
                error_msg = response.json().get("error", "خطا در توقف بازی.")
                messagebox.showerror("خطا", error_msg)
        except Exception as e:
            messagebox.showerror("خطا", f"خطای شبکه:\n{e}")

    def resume_game(self):
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"http://127.0.0.1:8000/api/games/{self.game_id}/resume/"

        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                self.game_status = "active"
                self.lbl_msg.configure(text="بازی ادامه یافت.", foreground="green")
                self.update_ui()
            else:
                error_msg = response.json().get("error", "خطا در ادامه بازی.")
                messagebox.showerror("خطا", error_msg)
        except Exception as e:
            messagebox.showerror("خطا", f"خطای شبکه:\n{e}")


    def update_game_status(self):
    # دریافت آخرین وضعیت بازی و بروزرسانی UI
     token = get_token()
     headers = {"Authorization": f"Bearer {token}"}
     url = f"http://127.0.0.1:8000/api/games/{self.game_id}/status/"

     try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.masked_word = data.get("masked_word", self.masked_word)
            self.turn_username = data.get("turn", self.turn_username)
            self.your_score = data.get("your_score", self.your_score)
            self.update_ui()
        else:
            messagebox.showerror("خطا", "خطا در دریافت وضعیت بازی")
     except Exception as e:
        messagebox.showerror("خطا", f"خطای شبکه:\n{e}")
