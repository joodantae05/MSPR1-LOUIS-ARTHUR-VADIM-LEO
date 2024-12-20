import tkinter as tk
from home_page import HomePage
from stats_page import StatsPage
from dashboard_page import DashboardPage
from ping_page import PingPage

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Seahawks Harvester")

        # Initialiser les pages
        self.home_page = HomePage(self.root, self)
        self.stats_page = StatsPage(self.root, self)
        self.dashboard_page = DashboardPage(self.root, self)
        self.ping_page = PingPage(self.root, self)

        # Afficher la page d'accueil par défaut
        self.show_home_page()

    def show_home_page(self):
        """Affiche la page d'accueil"""
        self.stats_page.hide()
        self.dashboard_page.hide()
        self.ping_page.hide()
        self.home_page.show()

    def show_stats_page(self):
        """Affiche la page des statistiques"""
        self.home_page.hide()
        self.dashboard_page.hide()
        self.ping_page.hide()
        self.stats_page.show()

    def show_dashboard_page(self):
        """Affiche la page du tableau de bord"""
        self.home_page.hide()
        self.stats_page.hide()
        self.ping_page.hide()
        self.dashboard_page.show()

    def show_ping_page(self):
        """Affiche la page de Ping"""
        self.home_page.hide()
        self.stats_page.hide()
        self.dashboard_page.hide()
        self.ping_page.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
