import ttkbootstrap as ttkb
from tkinter import messagebox
import requests
from app_token import get_token

class ActualGamePage(ttkb.Frame):
    def __init__(self, master, game_id, player1, player2, word_length, turn_username, show_main_menu_callback, show_history_page_callback):
        super().__init__(master)
        self.master = master
        self.game_id = game_id
        self.player1 = player1
        self.player2 = player2
        self.word_length = word_length
        self.game_status = "active"
        self.turn_username = turn_username
        self.show_main_menu_callback = show_main_menu_callback
        self.show_history_page_callback = show_history_page_callback
        
        self.masked_word = "_" * word_length
        self.your_username = getattr(master, 'username', None) or ""
        self.your_score = 0
        self.game_finished = False

        self.build_ui()
        self.poll_game_status()

    def build_ui(self):
        # عنوان اصلی
        ttkb.Label(self, text="🎯 بازی حدس کلمه", font=("B Nazanin", 26, "bold"), bootstyle="primary").pack(pady=(20,10))

        # نمایش کلمه پنهان شده با فاصله بیشتر و فونت درشت‌تر
        self.lbl_masked_word = ttkb.Label(self, text=' '.join(self.masked_word.upper()), font=("B Nazanin", 48, "bold"), bootstyle="info-inverse")
        self.lbl_masked_word.pack(pady=20, ipadx=15, ipady=10)

        # فریم اطلاعات بازیکن‌ها و امتیاز
        info_frame = ttkb.Frame(self)
        info_frame.pack(pady=10, fill="x", padx=20)

        # نوبت بازی
        self.lbl_turn = ttkb.Label(info_frame, text=f"🔄 نوبت: {self.turn_username}", font=("B Nazanin", 18), bootstyle="warning")
        self.lbl_turn.pack(side="left", padx=10)

        # امتیاز شما
        self.lbl_score = ttkb.Label(info_frame, text=f"⭐ امتیاز شما: {self.your_score}", font=("B Nazanin", 18), bootstyle="info")
        self.lbl_score.pack(side="right", padx=10)

        # فریم ورودی حرف و دکمه حدس
        input_frame = ttkb.Frame(self)
        input_frame.pack(pady=15)

        ttkb.Label(input_frame, text="🔤 حرف را وارد کنید:", font=("B Nazanin", 16)).pack(side="left", padx=(0,10))

        self.letter_var = ttkb.StringVar()
        self.entry_letter = ttkb.Entry(input_frame, textvariable=self.letter_var, width=4, font=("B Nazanin", 24), justify="center")
        self.entry_letter.pack(side="left")
        self.entry_letter.focus()

        self.btn_guess = ttkb.Button(input_frame, text="🎯 حدس بزن", bootstyle="success", command=self.send_guess)
        self.btn_guess.pack(side="left", padx=15)

        # پیام وضعیت حدس
        self.lbl_msg = ttkb.Label(self, text="", font=("B Nazanin", 16, "bold"))
        self.lbl_msg.pack(pady=10)

        # دکمه‌های توقف و ادامه بازی در یک فریم کنار هم
        control_frame = ttkb.Frame(self)
        control_frame.pack(pady=10)

        self.btn_pause = ttkb.Button(control_frame, text="⏸ توقف بازی", bootstyle="warning-outline", command=self.pause_game, width=15)
        self.btn_pause.pack(side="left", padx=10)

        self.btn_resume = ttkb.Button(control_frame, text="▶ ادامه بازی", bootstyle="primary-outline", command=self.resume_game, width=15)
        self.btn_resume.pack(side="left", padx=10)
        self.btn_resume.configure(state="disabled")

        # دکمه بازگشت به منو با رنگ و فونت برجسته‌تر
        ttkb.Button(self, text="🏠 بازگشت به منو", bootstyle="danger", command=self.show_main_menu_callback, width=20).pack(pady=20)

    def send_guess(self):
        if self.game_finished:
            return

        letter = self.letter_var.get().strip().lower()
        if len(letter) != 1 or not letter.isalpha():
            messagebox.showwarning("هشدار", "لطفاً فقط یک حرف معتبر وارد کنید.")
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
                    self.lbl_msg.configure(text="✅ حدس درست بود!", foreground="#2e7d32")  # سبز تیره
                else:
                    self.lbl_msg.configure(text="❌ حدس نادرست بود!", foreground="#c62828")  # قرمز تیره

                if game_status == "finished":
                    self.handle_game_finished(data)
            else:
                error_msg = response.json().get("error", "خطا در ارسال حدس.")
                messagebox.showerror("خطا", error_msg)
        except Exception as e:
            messagebox.showerror("خطا", f"خطای شبکه:\n{e}")

        self.letter_var.set("")
        self.entry_letter.focus()

    def update_ui(self):
        self.lbl_masked_word.configure(text=' '.join(self.masked_word.upper()))
        self.lbl_turn.configure(text=f"🔄 نوبت: {self.turn_username}")
        self.lbl_score.configure(text=f"⭐ امتیاز شما: {self.your_score}")

        if self.game_status == "paused":
            self.entry_letter.configure(state="disabled")
            self.btn_guess.configure(state="disabled")
            self.btn_pause.configure(state="disabled")
            self.btn_resume.configure(state="normal")
            self.lbl_msg.configure(text="⏸ بازی متوقف است.", foreground="#f9a825")  # زرد قوی
        else:
            self.entry_letter.configure(state="normal")
            self.btn_guess.configure(state="normal")
            self.btn_pause.configure(state="normal")
            self.btn_resume.configure(state="disabled")

    def handle_game_finished(self, data):
     if self.game_finished:
        return
     self.game_finished = True

     winner = data.get("winner")
     player1 = data.get("player1")
     player2 = data.get("player2")
     player1_score = data.get("player1_score", 0)
     player2_score = data.get("player2_score", 0)

     your_score = player1_score if self.your_username == player1 else player2_score

     if winner is None:
        message = f"🤝 بازی مساوی شد!\nامتیازها: {player1_score} - {player2_score}"
     elif self.your_username == winner:
        message = f"🎉 تبریک! شما برنده شدید! 🏆\nامتیاز شما: {your_score}"
     else:
        message = f"😞 متاسفانه بازنده شدید.\nبرنده بازی: {winner}\nامتیاز شما: {your_score}"

     messagebox.showinfo("🏁 پایان بازی", message)
     self.show_history_page_callback()



    def poll_game_status(self):
        if self.game_finished:
            return

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

                updated = False

                if masked_word != self.masked_word:
                    self.masked_word = masked_word
                    updated = True

                if turn != self.turn_username:
                    self.turn_username = turn
                    updated = True

                if your_score != self.your_score:
                    self.your_score = your_score
                    updated = True

                self.game_status = status

                if updated:
                    self.update_ui()

                if status == "finished":
                    self.handle_game_finished(data)
                    return  # دیگه polling رو ادامه نده

        except Exception as e:
            print("خطا در polling:", e)

        self.after(2500, self.poll_game_status)  # دوباره اجرا بعد ۳ ثانیه

    def pause_game(self):
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"http://127.0.0.1:8000/api/games/{self.game_id}/pause/"

        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                self.game_status = "paused"
                self.lbl_msg.configure(text="⏸ بازی متوقف شد.", foreground="#f9a825")
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
                self.lbl_msg.configure(text="▶ بازی ادامه یافت.", foreground="#2e7d32")
                self.update_ui()
            else:
                error_msg = response.json().get("error", "خطا در ادامه بازی.")
                messagebox.showerror("خطا", error_msg)
        except Exception as e:
            messagebox.showerror("خطا", f"خطای شبکه:\n{e}")
