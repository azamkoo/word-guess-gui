import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import StringVar, messagebox
import requests
from app_token import get_token, get_user

class ActualGamePage(ttkb.Frame):
    def __init__(self, master, game_id, player1, player2, word_length, turn_username, show_main_menu_callback):
        super().__init__(master)
        self.game_id = game_id
        self.player1 = player1
        self.player2 = player2
        self.word_length = word_length
        self.turn_username = turn_username
        self.show_main_menu_callback = show_main_menu_callback
        self.masked_word = "_" * word_length  # Track the current state of the word

        # Layout container
        container = ttkb.Frame(self)
        container.pack(expand=True, fill="both", padx=20, pady=20)

        # Players display
        players_lbl = f"{player1} vs {player2}"
        ttkb.Label(
            container, 
            text=players_lbl, 
            font=("B Nazanin", 20, "bold"),
            bootstyle="primary"
        ).pack(pady=10)

        # Turn indicator
        self.turn_label = ttkb.Label(
            container, 
            text=f"نوبت: {turn_username}", 
            font=("B Nazanin", 16),
            bootstyle="info"
        )
        self.turn_label.pack(pady=10)

        # Placeholders for the word
        self.placeholders = []
        placeholder_frame = ttkb.Frame(container)
        placeholder_frame.pack(pady=30)
        for _ in range(word_length):
            lbl = ttkb.Label(
                placeholder_frame, 
                text="_", 
                font=("Arial", 36, "bold"), 
                width=2, 
                bootstyle="secondary"
            )
            lbl.pack(side="left", padx=8)
            self.placeholders.append(lbl)

        # Input for guessing
        input_frame = ttkb.Frame(container)
        input_frame.pack(pady=10)
        
        ttkb.Label(
            input_frame, 
            text="حرف خود را وارد کنید:", 
            font=("B Nazanin", 14)
        ).pack(side="left", padx=5)
        
        self.guess_var = StringVar()
        self.guess_entry = ttkb.Entry(
            input_frame, 
            textvariable=self.guess_var, 
            width=5, 
            font=("Arial", 16),
            justify="center"
        )
        self.guess_entry.pack(side="left", padx=5)
        
        self.guess_button = ttkb.Button(
            input_frame, 
            text="ثبت حدس", 
            bootstyle="success", 
            command=self.guess_letter
        )
        self.guess_button.pack(side="left", padx=5)
        
        # Bind Enter key to guess submission
        self.guess_entry.bind("<Return>", lambda e: self.guess_letter())

        # Guessed letters display
        self.guessed_letters_label = ttkb.Label(
            container,
            text="حروف حدس زده شده: -",
            font=("B Nazanin", 12)
        )
        self.guessed_letters_label.pack(pady=10)

        # Return to menu button
        ttkb.Button(
            container, 
            text="بازگشت به منو", 
            bootstyle="danger", 
            command=show_main_menu_callback
        ).pack(pady=20)

    def guess_letter(self):
        token = get_token()
        current_user = get_user()
        
        # Validate input
        letter = self.guess_var.get().strip().lower()
        if not letter or len(letter) != 1 or not letter.isalpha():
            messagebox.showwarning("خطا", "لطفاً فقط یک حرف معتبر وارد کنید.")
            return

        if letter in self.masked_word:
            messagebox.showwarning("خطا", "این حرف قبلاً حدس زده شده است.")
            return

        try:
            # Make API request
            response = requests.post(
                f"http://127.0.0.1:8000/api/games/{self.game_id}/guess/",
                json={"letter": letter},
                headers={'Authorization': f'Bearer {token}'},
                timeout=5
            )

            # Handle response
            if response.status_code == 404:
                messagebox.showerror("خطا", "آدرس API یافت نشد. لطفاً تنظیمات سرور را بررسی کنید.")
                return

            data = response.json()

            if response.status_code == 200:
                # Update game state
                self.masked_word = data.get("masked_word", self.masked_word)
                self.update_placeholders()
                
                # Update turn
                self.turn_username = data.get("turn", self.turn_username)
                self.turn_label.config(text=f"نوبت: {self.turn_username}")
                
                # Update guessed letters
                guessed_letters = ", ".join(sorted(set(self.masked_word.replace("_", ""))))
                self.guessed_letters_label.config(text=f"حروف حدس زده شده: {guessed_letters or '-'}")
                
                # Check if game ended
                if data.get("status") == "finished":
                    winner = data.get("winner")
                    message = "شما برنده شدید! 🎉" if winner == current_user else f"{winner} برنده شد!"
                    messagebox.showinfo("پایان بازی", message)
                    self.show_main_menu_callback()
            else:
                messagebox.showerror("خطا", data.get("error", "خطای نامشخص از سرور"))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("خطای ارتباط", f"مشکل در ارتباط با سرور:\n{str(e)}")
        except ValueError:
            messagebox.showerror("خطا", "پاسخ نامعتبر از سرور دریافت شد")
        finally:
            self.guess_var.set("")
            self.guess_entry.focus()

    def update_placeholders(self):
        for i, char in enumerate(self.masked_word):
            if char != '_':
                self.placeholders[i].config(
                    text=char.upper(),
                    bootstyle="success"
                )