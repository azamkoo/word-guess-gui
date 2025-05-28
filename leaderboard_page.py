import ttkbootstrap as ttkb
from tkinter import messagebox
import requests
from app_token import get_token

class LeaderboardPage(ttkb.Frame):
    def __init__(self, master, show_menu_callback):
        super().__init__(master)
        self.master = master
        self.show_menu_callback = show_menu_callback

        ttkb.Label(
            self, 
            text="🏆 لیست برترین بازیکنان", 
            font=("B Nazanin", 26, "bold"), 
            bootstyle="primary"
        ).pack(pady=20)

        style = ttkb.Style()

        # فقط استایل فونت و رنگ ستون‌ها رو بهتر می‌کنیم، بدون تغییر خاص
        style.configure("Treeview",
                        font=("B Nazanin", 12),
                        foreground="#222",
                        background="#f9f9f9",
                        fieldbackground="#f9f9f9")
        style.map("Treeview", background=[("selected", "#3399ff")], foreground=[("selected", "white")])

        self.table = ttkb.Treeview(
            self, 
            columns=("rank", "username", "score", "level", "xp", "win_rate"),
            show="headings", 
            height=15,
            style="Treeview"
        )

        self.table.heading("rank", text="رتبه")
        self.table.heading("username", text="نام کاربری")
        self.table.heading("score", text="امتیاز")
        self.table.heading("level", text="سطح")
        self.table.heading("xp", text="تجربه")
        self.table.heading("win_rate", text="نرخ برد")

        self.table.column("rank", width=60, anchor="center")
        self.table.column("username", width=150, anchor="center")
        self.table.column("score", width=80, anchor="center")
        self.table.column("level", width=80, anchor="center")
        self.table.column("xp", width=100, anchor="center")
        self.table.column("win_rate", width=100, anchor="center")

        self.table.pack(pady=10, padx=10, fill="both", expand=True)

        ttkb.Button(
            self, 
            text="بازگشت به منوی اصلی", 
            bootstyle="secondary", 
            command=self.show_menu_callback,
            width=25
        ).pack(pady=15)

        self.fetch_leaderboard()

    def fetch_leaderboard(self):
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}
        url = "http://127.0.0.1:8000/api/leaderboard/"

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                for player in data:
                    self.table.insert("", "end", values=(
                        player.get("rank"),
                        player.get("username"),
                        player.get("score"),
                        player.get("level"),
                        player.get("xp"),
                        player.get("win_rate"),
                    ))
            else:
                messagebox.showerror("خطا", "خطا در دریافت اطلاعات لیدربورد.")
        except Exception as e:
            messagebox.showerror("خطای شبکه", str(e))
