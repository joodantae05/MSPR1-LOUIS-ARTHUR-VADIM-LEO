import tkinter as tk
from tkinter import ttk
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
        window_width = 1200
        window_height = 800

        # Centrer la fenêtre
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculer les positions pour centrer la fenêtre
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Appliquer la géométrie de la fenêtre et la position centrale
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.root.config(bg="#1e1e2f")  # Arrière-plan sombre moderne

        # Créer un cadre principal pour le contenu
        self.main_frame = tk.Frame(self.root, bg="#1e1e2f")
        self.main_frame.pack(fill="both", expand=True)

        # Créer un cadre pour le header (titre + onglets)
        self.header_frame = tk.Frame(self.main_frame, bg="#1e1e2f")
        self.header_frame.pack(fill="x", pady=(20, 10), padx=30)

        # Ajouter un titre centré
        self.title_label = tk.Label(self.header_frame, text="Seahawks Harvester", font=("Helvetica", 28, "bold"), bg="#1e1e2f", fg="#fff")
        self.title_label.pack(side="left", padx=20)

        # Créer un cadre pour les onglets (navigation horizontale)
        self.tabs_frame = tk.Frame(self.header_frame, bg="#1e1e2f")
        self.tabs_frame.pack(side="right", padx=30)

        # Créer les boutons de navigation
        self.home_button = self.create_tab_button(self.tabs_frame, "Home", self.show_home_page)
        self.stats_button = self.create_tab_button(self.tabs_frame, "Stats", self.show_stats_page)
        self.dashboard_button = self.create_tab_button(self.tabs_frame, "Dashboard", self.show_dashboard_page)
        self.ping_button = self.create_tab_button(self.tabs_frame, "Ping", self.show_ping_page)

        # Label pour afficher l'heure, positionné au centre du header
        self.clock_label = tk.Label(self.header_frame, text=self.get_current_time(), font=("Helvetica", 16), bg="#1e1e2f", fg="#fff")
        self.clock_label.pack(side="left", padx=40, expand=True)

        # Créer un bouton "Go" central
        self.go_button = tk.Button(self.main_frame, text="Go", font=("Helvetica", 36, "bold"), command=self.animate_go_button,
                                   bg="#1786dc", fg="#fff", bd=0, relief="flat", padx=40, pady=20, activebackground="#0a5f97")
        self.go_button.place(relx=0.5, rely=0.5, anchor="center")  # Centrer le bouton

        # Initialiser les pages
        self.dashboard_page = DashboardPage(self.main_frame, self)
        self.stats_page = StatsPage(self.main_frame, self)
        self.home_page = HomePage(self.main_frame, self, self.dashboard_page, self.stats_page)
        self.ping_page = PingPage(self.main_frame, self)

        # Afficher la page d'accueil par défaut
        self.show_home_page()

        # Mettre à jour l'heure chaque seconde
        self.update_clock()

    def create_tab_button(self, parent, text, command):
        """Fonction pour créer un bouton de navigation avec surbrillance moderne"""
        button = tk.Button(parent, text=text, font=("Helvetica", 14), bg="#1e1e2f", fg="#d9d7dc", bd=0, relief="flat", padx=20, pady=10,
                           activebackground="#1786dc", activeforeground="#fff", command=command)
        button.pack(side="left", padx=20)
        button.bind("<Enter>", lambda event: button.config(fg="#1786dc"))
        button.bind("<Leave>", lambda event: button.config(fg="#d9d7dc"))
        return button

    def get_current_time(self):
        """Retourne l'heure actuelle sous forme de chaîne"""
        return time.strftime('%H:%M:%S')

    def update_clock(self):
        """Met à jour l'heure sur l'interface"""
        current_time = self.get_current_time()
        self.clock_label.config(text=current_time)  # Mettre à jour le label avec l'heure actuelle
        self.root.after(1000, self.update_clock)  # Réactualiser toutes les 1000ms (1 seconde)

    def animate_go_button(self):
        """Animation dynamique pour le bouton Go"""
        colors = ["#00bcd4", "#4caf50", "#ffeb3b", "#f44336", "#00bcd4"]
        for color in colors:
            self.go_button.config(bg=color)
            self.root.update()
            time.sleep(0.1)

    def show_home_page(self):
        """Affiche la page d'accueil et met en surbrillance le bouton Home"""
        self.stats_page.hide()
        self.dashboard_page.hide()
        self.ping_page.hide()
        self.home_page.show()

        # Mettre à jour la surbrillance des onglets
        self.update_tab_highlight(self.home_button)

    def show_stats_page(self):
        """Affiche la page des statistiques"""
        self.home_page.hide()
        self.dashboard_page.hide()
        self.ping_page.hide()
        self.stats_page.show()

        # Mettre à jour la surbrillance des onglets
        self.update_tab_highlight(self.stats_button)

    def show_dashboard_page(self):
        """Affiche la page du tableau de bord"""
        self.home_page.hide()
        self.stats_page.hide()
        self.ping_page.hide()
        self.dashboard_page.show()

        # Mettre à jour la surbrillance des onglets
        self.update_tab_highlight(self.dashboard_button)

    def show_ping_page(self):
        """Affiche la page de Ping"""
        self.home_page.hide()
        self.stats_page.hide()
        self.dashboard_page.hide()
        self.ping_page.show()

        # Mettre à jour la surbrillance des onglets
        self.update_tab_highlight(self.ping_button)

    def update_tab_highlight(self, active_button):
        """Met à jour la surbrillance du bouton actif et réinitialise les autres boutons"""
        buttons = [self.home_button, self.stats_button, self.dashboard_button, self.ping_button]
        for button in buttons:
            if button == active_button:
                button.config(fg="#fff", bg="#1786dc", bd=2)  # Surbrillance du bouton actif
            else:
                button.config(fg="#d9d7dc", bg="#1e1e2f", bd=0)  # Réinitialiser les autres boutons

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
