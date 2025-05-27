# main.py
import requests
import ttkbootstrap as ttkb

from app_token import get_token
from game_board import ActualGamePage
from join_game_page import JoinGamePage
from my_games_history_page import MyGamesHistoryPage
from start_page import StartPage
from register_page import RegisterPage
from login_page import LoginPage
from profile_page import ProfilePage
from main_menu_page import MainMenuPage
from create_game_page import CreateGamePage


class App(ttkb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("بازی حدس کلمه 🎮")
        self.geometry("600x600")
        self.state('zoomed')

        self.start_page = StartPage(self, self.show_register_page, self.show_login_page, self.exit_app)
        self.register_page = RegisterPage(self, self.show_login_page)
        self.login_page = LoginPage(self, self.show_register_page, self.after_login_success)
        self.profile_page = None
        self.main_menu_page = None
        self.actual_game_page = None
        self.current_frame = None
        self.show_frame(self.start_page)

        self.main_menu_page = MainMenuPage(
            self,
            create_game_callback=self.show_create_game_page,
            join_game_callback=self.show_join_game_page,
            show_history_callback=self.show_history_page,
            logout_callback=self.handle_logout,
            show_profile_callback=self.after_login_success
        )
        

    def show_frame(self, frame):
        if self.current_frame:
            self.current_frame.pack_forget()
        self.current_frame = frame
        self.current_frame.pack(fill="both", expand=True)

    def show_register_page(self):
        self.show_frame(self.register_page)

    def show_login_page(self):
        self.show_frame(self.login_page)

    def after_login_success(self):
        self.profile_page = ProfilePage(
            self,
            show_menu_callback=self.show_menu_page,  # new
            show_logout_callback=self.handle_logout
        )
        self.show_frame(self.profile_page)

    def handle_logout(self):
        self.show_frame(self.start_page)

    def show_menu_page(self):
        if not self.main_menu_page:
            self.main_menu_page = MainMenuPage(
                self,
                create_game_callback=self.show_create_game_page,
                join_game_callback=self.show_join_game_page,
                show_history_callback=self.show_history_page,
                show_profile_callback=self.after_login_success,
                logout_callback=self.handle_logout
            )
        self.show_frame(self.main_menu_page)

    def show_create_game_page(self):
        self.create_game_page = CreateGamePage(self, show_main_menu_callback=self.show_menu_page)
        self.show_frame(self.create_game_page)

    def start_actual_game(self, game_id):
        token = get_token()
        headers = {'Authorization': f'Bearer {token}'}
        try:
            resp = requests.get(f"http://127.0.0.1:8000/api/games/{game_id}/status/", headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                player1 = data.get("player1")
                player2 = data.get("player2")
                word_length = data.get("word_length", 4)  # You may need to add this to status API!
                turn = data.get("turn")  # May need to add this field too
                if not word_length:
                    word_length = 4
                if not turn:
                    turn = player1
                self.actual_game_page = ActualGamePage(
                    self,
                    game_id=game_id,
                    player1=player1,
                    player2=player2,
                    word_length=word_length,
                    turn_username=turn,
                    show_main_menu_callback=self.show_menu_page,
                    
                )
                self.show_frame(self.actual_game_page)
            else:
                from tkinter import messagebox
                messagebox.showerror("خطا", "دریافت اطلاعات بازی ناموفق بود.")
                self.show_menu_page()
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("خطا", str(e))
            self.show_menu_page()

    def show_join_game_page(self):
        self.join_game_page = JoinGamePage(self, show_main_menu_callback=self.show_menu_page,
                                           start_actual_game_callback=self.start_actual_game)
        self.show_frame(self.join_game_page)

    def show_history_page(self):
        self.my_games_history_page = MyGamesHistoryPage(self, show_menu_callback=self.show_menu_page)
        self.show_frame(self.my_games_history_page)

    def exit_app(self):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
