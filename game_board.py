import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import StringVar


class ActualGamePage(ttkb.Frame):
    def __init__(self, master, game_id, player1, player2, word_length, turn_username, show_main_menu_callback):
        super().__init__(master)
        self.game_id = game_id
        self.player1 = player1
        self.player2 = player2
        self.word_length = word_length
        self.turn_username = turn_username
        self.show_main_menu_callback = show_main_menu_callback

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

        guess_button = ttkb.Button(container, text="ثبت حدس", bootstyle="success", command=self.fake_guess)
        guess_button.pack(pady=10)

        # Return to menu (for testing)
        ttkb.Button(container, text="بازگشت به منو", bootstyle="danger", command=show_main_menu_callback).pack(pady=20)

    def fake_guess(self):
        # Just for now, show a popup; real logic will come later
        from tkinter import messagebox
        messagebox.showinfo("حدس ثبت شد", "در نسخه بعدی فعال می‌شود!")
