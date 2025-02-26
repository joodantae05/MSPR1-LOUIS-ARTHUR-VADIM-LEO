import tkinter as tk
import time

from home_page import HomePage
from stats_page import StatsPage
from dashboard_page import DashboardPage
from ping_page import PingPage

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Seahawks Harvester")

        # Définir la taille de la fenêtre
        window_width = 850
        window_height = 600

        # Centrer la fenêtre
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.root.config(bg="#121212")  # Arrière-plan sombre moderne
        self.root.resizable(False, False)  # Désactive le redimensionnement de la fenêtre

        # Frame principale (contenant tout)
        self.main_frame = tk.Frame(self.root, bg="#121212")
        self.main_frame.pack(fill="both", expand=True)

        # Titre centré
        self.title_label = tk.Label(self.main_frame, text="Seahawks Harvester", font=("Helvetica", 24, "bold"), bg="#1e1e2f" ,fg="#fff")
        self.title_label.pack(pady=30)

        # Ajouter un bouton "Go" animé
        self.go_button = tk.Button(self.main_frame, text="Go", font=("Helvetica", 36, "bold"), command=self.animate_go_button,
                                   bg="#1786dc", fg="#fff", bd=0, relief="flat", padx=15, pady=15, activebackground="#0a5f97")
        self.go_button.place(relx=0.5, rely=0.5, anchor="center")  # Centrer le bouton

        # Créer un cadre pour les boutons en bas
        self.footer_frame = tk.Frame(self.main_frame, bg="#121212")
        self.footer_frame.pack(side="bottom", fill="x", pady=(20, 20))

        # Créer les boutons de navigation en bas avec effets de survol
        self.home_button = self.create_tab_button(self.footer_frame, "Home", self.show_home_page)
        self.stats_button = self.create_tab_button(self.footer_frame, "Stats", self.show_stats_page)
        self.dashboard_button = self.create_tab_button(self.footer_frame, "Dashboard", self.show_dashboard_page)
        self.ping_button = self.create_tab_button(self.footer_frame, "Ping", self.show_ping_page)

        # Initialiser les pages
        self.dashboard_page = DashboardPage(self.main_frame, self)
        self.stats_page = StatsPage(self.main_frame, self)
        self.home_page = HomePage(self.main_frame, self, self.dashboard_page, self.stats_page)
        self.ping_page = PingPage(self.main_frame, self)

        # Afficher la page d'accueil par défaut
        self.show_home_page()

    def create_tab_button(self, parent, text, command):
        """Fonction pour créer un bouton de navigation moderne avec surbrillance fluide"""
        button = tk.Button(parent, text=text, font=("Helvetica", 14), bg="#121212", fg="#d9d7dc", bd=0, relief="flat", padx=20, pady=10,
                           activebackground="#1786dc", activeforeground="#fff", command=command)
        button.pack(side="left", padx=15)
        button.bind("<Enter>", lambda event: button.config(fg="#00bcd4"))
        button.bind("<Leave>", lambda event: button.config(fg="#d9d7dc"))
        return button

    def animate_go_button(self):
        """Animation fluide pour le bouton Go"""
        colors = ["#00bcd4", "#4caf50", "#ffeb3b", "#f44336", "#00bcd4"]
        for color in colors:
            self.go_button.config(bg=color)
            self.root.update_idletasks()  # Mise à jour pour éviter des ralentissements
            time.sleep(0.1)

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
