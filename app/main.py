import tkinter as tk
from home_page import HomePage
from stats_page import StatsPage
from dashboard_page import DashboardPage
from ping_page import PingPage

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Seahawks Harvester")
        self.root.geometry("1200x800+{}+{}".format(
            (self.root.winfo_screenwidth() - 1200) // 2, 
            (self.root.winfo_screenheight() - 800) // 2
        ))
        self.root.config(bg="#121212")
        self.root.resizable(False, False)

        self.main_frame = tk.Frame(self.root, bg="#121212")
        self.main_frame.pack(fill="both", expand=True)

        self.title_label = tk.Label(self.main_frame, text="Seahawks Harvester", font=("Helvetica", 24, "bold"), bg="#1e1e2f", fg="#fff")
        self.title_label.pack(pady=30)

        self.footer_frame = tk.Frame(self.main_frame, bg="#121212")
        self.footer_frame.pack(side="bottom", fill="x", pady=(20, 20))

        # Buttons de navigation
        self.home_button = self.create_tab_button("Home", self.show_home_page)
        self.stats_button = self.create_tab_button("Stats", self.show_stats_page)
        self.dashboard_button = self.create_tab_button("Dashboard", self.show_dashboard_page)
        self.ping_button = self.create_tab_button("Ping", self.show_ping_page)

        # Pages
        self.dashboard_page = DashboardPage(self.main_frame, self)
        self.stats_page = StatsPage(self.main_frame, self)
        self.home_page = HomePage(self.main_frame, self, self.dashboard_page, self.stats_page)
        self.ping_page = PingPage(self.main_frame, self)

        self.show_home_page()

    def create_tab_button(self, text, command):
        """Création des boutons de navigation"""
        button = tk.Button(self.footer_frame, text=text, font=("Helvetica", 14), bg="#121212", fg="#d9d7dc", bd=0, relief="flat", padx=20, pady=10, command=command)
        button.pack(side="left", padx=15)
        button.bind("<Enter>", lambda event: button.config(fg="#00bcd4"))
        button.bind("<Leave>", lambda event: button.config(fg="#d9d7dc"))
        return button

    def show_home_page(self):
        self.stats_page.hide()
        self.dashboard_page.hide()
        self.ping_page.hide()
        self.home_page.show()

    def show_stats_page(self):
        self.home_page.hide()
        self.dashboard_page.hide()
        self.ping_page.hide()
        self.stats_page.show()

    def show_dashboard_page(self):
        self.home_page.hide()
        self.stats_page.hide()
        self.ping_page.hide()
        self.dashboard_page.show()

    def show_ping_page(self):
        self.home_page.hide()
        self.stats_page.hide()
        self.dashboard_page.hide()
        self.ping_page.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
