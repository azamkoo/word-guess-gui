import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import StringVar
import requests
from tkinter import messagebox

class ActualGamePage(ttkb.Frame):
    def __init__(self, master, game_id, player1, player2, word_length, turn_username, show_main_menu_callback , auth_token):
        super().__init__(master)
        self.game_id = game_id
        self.player1 = player1
        self.player2 = player2
        self.word_length = word_length
        self.turn_username = turn_username
        self.show_main_menu_callback = show_main_menu_callback
        self.auth_token = auth_token


        # Layout container
        container = ttkb.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Players display
        players_lbl = f"{player1} vs {player2}"
        ttkb.Label(container, text=players_lbl, font=("B Nazanin", 20, "bold")).pack(pady=10)

        # Turn indicator
        self.turn_label = ttkb.Label(container, text=f"نوبت: {turn_username}", font=("B Nazanin", 16))
        self.turn_label.pack(pady=10)

        # Placeholders for the word
        self.placeholders = []
        placeholder_frame = ttkb.Frame(container)
        placeholder_frame.pack(pady=30)
        for _ in range(word_length):
            lbl = ttkb.Label(placeholder_frame, text="_", font=("Arial", 36, "bold"), width=2, bootstyle="secondary")
            lbl.pack(side="left", padx=8)
            self.placeholders.append(lbl)

        # Input for guessing (not functional yet)
        guess_label = ttkb.Label(container, text="حرف خود را وارد کنید:", font=("B Nazanin", 14))
        guess_label.pack(pady=5)
        self.guess_var = StringVar()
        guess_entry = ttkb.Entry(container, textvariable=self.guess_var, width=5, font=("Arial", 16))
        guess_entry.pack(pady=5)

        guess_button = ttkb.Button(container, text="ثبت حدس", bootstyle="success", command=self.guess_letter)
        guess_button.pack(pady=10)

        # Return to menu (for testing)
        ttkb.Button(container, text="بازگشت به منو", bootstyle="danger", command=show_main_menu_callback).pack(pady=20)

    def guess_letter(self):
     letter = self.guess_var.get().strip().lower()
     if not letter or len(letter) != 1 or not letter.isalpha():
        messagebox.showwarning("خطا", "لطفاً فقط یک حرف وارد کنید.")
        return

     try:
        response = requests.post(
            f"http://127.0.0.1:8000/games/{self.game_id}/guess/",
            json={"letter": letter},
            headers={"Authorization": f"Token {self.master.auth_token}"}
        )
        data = response.json()

        if response.status_code == 200:
            # Correct or incorrect guess
            new_masked_word = data.get("masked_word")  # Optional enhancement: return this in your API
            self.update_placeholders(new_masked_word)

            if data.get("status") == "finished":
                messagebox.showinfo("🎉 پایان بازی", "شما کلمه را کامل کردید!")
                self.show_main_menu_callback()
            else:
                self.turn_username = data.get("turn_username")
                self.turn_label.config(text=f"نوبت: {self.turn_username}")
        else:
            messagebox.showerror("خطا", data.get("error", "مشکلی پیش آمده."))

     except Exception as e:
        messagebox.showerror("خطا", f"مشکل در ارتباط با سرور:\n{e}")

def update_placeholders(self, masked_word):
    for i, char in enumerate(masked_word):
        self.placeholders[i].config(text=char if char != '_' else '_')

