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

        # Définir la taille de la fenêtre et la couleur de fond
        self.root.geometry("1080x720")
        self.root.config(bg="#141526")  # Couleur de fond #141526
        
        # Créer un cadre pour l'ensemble du contenu avec un fond uniforme
        self.main_frame = tk.Frame(self.root, bg="#141526")
        self.main_frame.pack(fill="both", expand=True)  # Ce cadre occupe tout l'espace disponible

        # Créer un cadre pour le titre et les onglets (alignés horizontalement)
        self.header_frame = tk.Frame(self.main_frame, bg="#141526")
        self.header_frame.pack(fill="x", padx=10, pady=10)  # Remplir horizontalement et espacer légèrement

        # Ajouter le titre à gauche
        self.title_label = tk.Label(self.header_frame, text="Seahawks Vester", font=("Helvetica", 24, "bold"), bg="#141526", fg="#d9d7dc")
        self.title_label.pack(side="left", padx=10)

        # Créer des boutons pour les onglets à droite
        self.tabs_frame = tk.Frame(self.header_frame, bg="#141526")
        self.tabs_frame.pack(side="right", fill="x", padx=10)  # Remplir l'espace restant horizontalement

        # Fonction pour changer la couleur du texte au survol
        def on_enter(button):
            button.config(fg="#1786dc")
            button.config(cursor="hand2")  # Changer le curseur au survol

        def on_leave(button):
            button.config(fg="#d9d7dc")
            button.config(cursor="arrow")  # Revenir au curseur normal

        # Ajouter les boutons pour naviguer entre les pages
        self.home_button = tk.Button(self.tabs_frame, text="Home", command=self.show_home_page, 
                                     bg="#141526", fg="#d9d7dc", font=("Helvetica", 12), bd=0,
                                     highlightthickness=0)  # Suppression de l'encadré
        self.home_button.pack(side="left", padx=10)
        self.home_button.bind("<Enter>", lambda event: on_enter(self.home_button))
        self.home_button.bind("<Leave>", lambda event: on_leave(self.home_button))

        self.stats_button = tk.Button(self.tabs_frame, text="Stats", command=self.show_stats_page, 
                                      bg="#141526", fg="#d9d7dc", font=("Helvetica", 12), bd=0,
                                      highlightthickness=0)  # Suppression de l'encadré
        self.stats_button.pack(side="left", padx=10)
        self.stats_button.bind("<Enter>", lambda event: on_enter(self.stats_button))
        self.stats_button.bind("<Leave>", lambda event: on_leave(self.stats_button))

        self.dashboard_button = tk.Button(self.tabs_frame, text="Dashboard", command=self.show_dashboard_page, 
                                          bg="#141526", fg="#d9d7dc", font=("Helvetica", 12), bd=0,
                                          highlightthickness=0)  # Suppression de l'encadré
        self.dashboard_button.pack(side="left", padx=10)
        self.dashboard_button.bind("<Enter>", lambda event: on_enter(self.dashboard_button))
        self.dashboard_button.bind("<Leave>", lambda event: on_leave(self.dashboard_button))

        self.ping_button = tk.Button(self.tabs_frame, text="Ping", command=self.show_ping_page, 
                                     bg="#141526", fg="#d9d7dc", font=("Helvetica", 12), bd=0,
                                     highlightthickness=0)  # Suppression de l'encadré
        self.ping_button.pack(side="left", padx=10)
        self.ping_button.bind("<Enter>", lambda event: on_enter(self.ping_button))
        self.ping_button.bind("<Leave>", lambda event: on_leave(self.ping_button))

        # Ajouter un bouton Go au centre avec animation en vague
        self.go_button = tk.Button(self.main_frame, text="Go", font=("Helvetica", 24, "bold"), command=self.animate_go_button, 
                                   bg="#141526", fg="#d9d7dc", bd=0, highlightthickness=0)  # Suppression de l'encadré
        self.go_button.place(relx=0.5, rely=0.5, anchor="center")  # Placer le bouton au centre de la fenêtre

        # Initialiser les pages dans l'ordre correct
        self.dashboard_page = DashboardPage(self.main_frame, self)
        self.home_page = HomePage(self.main_frame, self, self.dashboard_page)  # Maintenant self.dashboard_page est disponible
        self.stats_page = StatsPage(self.main_frame, self)
        self.ping_page = PingPage(self.main_frame, self)

        # Afficher la page d'accueil par défaut
        self.show_home_page()

    def animate_go_button(self):
        """Animation dynamique en vague pour le bouton Go"""
        colors = ["lightblue", "lightgreen", "lightyellow", "lightcoral", "lightblue"]
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
                button.config(fg="#1786dc")  # Surbrillance du bouton actif
            else:
                button.config(fg="#d9d7dc")  # Réinitialiser les autres boutons

        # Activer ou désactiver le curseur selon la page
        for button in buttons:
            button.config(cursor="arrow")  # Réinitialiser le curseur par défaut

        active_button.config(cursor="hand2")  # Modifier le curseur sur l'onglet actif

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
