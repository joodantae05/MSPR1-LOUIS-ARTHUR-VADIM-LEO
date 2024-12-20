import socket
import ipaddress
import scapy.all as scapy
import threading
from tkinter import DISABLED, HORIZONTAL, NORMAL, Frame, Label, Button, Listbox, END
from tkinter.ttk import Progressbar
from base_page import BasePage
from utils import get_local_network, scan_network  # Vous pouvez déplacer ces fonctions dans un fichier utils.py

class HomePage(BasePage):
    def __init__(self, root, app):
        title = "Bienvenue sur Seahawks Harvester"
        tabs = {
            "Home": self.app.show_home_page,
            "Stats": self.app.show_stats_page,
            "Dashboard": self.app.show_dashboard_page,
            "Ping": self.app.show_ping_page
        }
        super().__init__(root, app, title, tabs)

        # Sous-titre
        self.subtitle_label = Label(
            self.frame,
            text="Scan du réseau local",
            font=("Helvetica", 14),
            fg="white",
            bg="#313438"
        )
        self.subtitle_label.pack(pady=10)

        # Bouton de lancement du scan
        self.scan_button = Button(
            self.frame,
            text="Démarrer le Scan",
            font=("Helvetica", 14),
            bg="#4CAF50",
            fg="white",
            command=self.start_scan
        )
        self.scan_button.pack(pady=20)

        # Barre de progression
        self.progress_bar = Progressbar(self.frame, orient=HORIZONTAL, length=400, mode="determinate")
        self.progress_bar.pack(pady=20)

        # Liste des hôtes en ligne
        self.host_list_label = Label(self.frame, text="Hôtes en ligne:", font=("Helvetica", 12), fg="white", bg="#313438")
        self.host_list_label.pack(pady=10)

        self.host_list = Listbox(self.frame, bg="#474B51", fg="white", height=10, width=50)
        self.host_list.pack(pady=10)

    def start_scan(self):
        """Démarre le scan du réseau local."""
        self.host_list.delete(0, END)  # Réinitialise la liste des hôtes
        self.progress_bar["value"] = 0  # Réinitialise la barre de progression
        self.scan_button.config(state=DISABLED)  # Désactive le bouton pendant le scan

        # Récupère le sous-réseau local
        local_network = get_local_network()

        # Lance le scan dans un thread pour éviter le blocage de l'interface
        threading.Thread(target=self.scan_and_update, args=(local_network,)).start()

    def scan_and_update(self, network_ip):
        """Effectue le scan et met à jour l'interface."""
        online_hosts = scan_network(str(network_ip), self.update_progress)

        # Mise à jour de l'interface avec les résultats du scan
        self.root.after(0, self.display_online_hosts, online_hosts)  # Mise à jour sur le thread principal

        # Réactive le bouton de scan
        self.root.after(0, self.scan_button.config, {"state": NORMAL})

    def update_progress(self, progress):
        """Met à jour la barre de progression."""
        self.progress_bar["value"] = progress * 100
        self.root.update_idletasks()

    def display_online_hosts(self, hosts):
        """Affiche les hôtes en ligne dans la liste."""
        for host in hosts:
            self.host_list.insert(END, host)
