import socket
import ipaddress
import tkinter as tk
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
import json
import os

from scan import scan_network, scan_ports  # Import des fonctions de scan
from dashboard_page import DashboardPage  # Import de la classe DashboardPage
from stats_page import StatsPage  # Import de la classe StatsPage

class HomePage:
    def __init__(self, root, app, dashboard, stats_page):
        self.root = root
        self.app = app
        self.dashboard = dashboard
        self.stats_page = stats_page  # Ajoutez la référence à StatsPage
        self.root.config(bg="#1E1E2D")  # Couleur de fond sombre

        # Créer le cadre principal
        self.frame = tk.Frame(root, bg="#1E1E2D")
        self.frame.pack(fill='both', expand=True, padx=20, pady=20)  # Espacement autour du cadre

        # Créer le bouton cliquable pour démarrer le scan
        self.button = tk.Button(self.frame, text="Démarrer le Scan", command=self.on_click,
                                relief="flat", bd=0, font=("Arial", 16), fg="white", bg="#4A90E2",
                                activebackground="#357ABD", activeforeground="white", width=20, height=2,
                                highlightthickness=0, pady=10)
        self.button.pack(pady=20)  # Centrer avec un peu d'espacement vertical

        # Initialiser la barre de progression
        self.progress_bar = ttk.Progressbar(self.frame, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)  # Espacement vertical

        # Initialiser le label pour le statut
        self.status_label = tk.Label(self.frame, text="Préparation du scan...", font=("Arial", 12), fg="white", bg="#1E1E2D")
        self.status_label.pack(pady=10)  # Espacement vertical

        self.times_per_host = []  # Liste des temps de scan par hôte pour ajuster les estimations

        # Variables pour les statistiques
        self.total_scans = 0
        self.avg_scan_time = 0
        self.most_vulnerable_host = "Aucun"

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

    def on_click(self):
        self.button.config(state="disabled")  # Désactiver le bouton pendant le scan
        threading.Thread(target=self.start_scan).start()  # Démarrer le scan dans un thread séparé

    def start_scan(self):
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = 100
        
        # Détecter l'adresse IP locale et déterminer le sous-réseau
        local_ip = self.get_local_ip()
        subnet = self.get_subnet(local_ip)

        # Scan réseau et récupération des hôtes en ligne
        online_hosts_gen, network = scan_network(str(subnet))  # Utiliser le sous-réseau détecté
        total_ips = sum(1 for _ in network.hosts())  # Nombre total d'IP à scanner
        
        # Scanner les ports des machines en ligne
        machine_info = []  # Liste pour stocker les informations des machines en ligne
        scanned_count = 0  # Compteur pour les machines scannées
        start_time = time.time()  # Commencer à chronométrer

        # Mise à jour périodique
        def update_periodically():
            elapsed_time = time.time() - start_time  # Temps écoulé
            elapsed_time_formatted = self.format_duration(elapsed_time)
            self.update_progress((scanned_count / len(online_hosts_gen)) * 100, elapsed_time_formatted)
            if scanned_count < len(online_hosts_gen):
                self.root.after(100, update_periodically)  # Mettre à jour toutes les 100ms (10 fois par seconde)

        # Lancer la mise à jour périodique
        self.root.after(100, update_periodically)

        # Traitement du scan des hôtes en ligne
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(scan_ports, ip): ip for ip in online_hosts_gen}
            for future in as_completed(futures):
                ip, open_ports, service_info, vulnerabilities = future.result()
                machine_info.append((ip, open_ports, service_info, vulnerabilities))

                # Calculer le temps de scan de l'hôte actuel et l'ajouter à la liste
                elapsed_time_per_host = time.time() - start_time - sum(self.times_per_host)
                self.times_per_host.append(elapsed_time_per_host)

                scanned_count += 1  # Incrémenter le compteur des machines scannées

        # Mise à jour du dashboard avec les résultats du scan
        self.update_dashboard(machine_info) 
        self.root.after(0, self.finish_scan)  # Appel pour terminer le scan et afficher les résultats

    def update_progress(self, progress_percentage, elapsed_time):
        """Mettre à jour la barre de progression et le label"""
        self.progress_bar["value"] = progress_percentage
        self.status_label.config(text=f"Scan en cours... Durée écoulée : {elapsed_time}")

    def finish_scan(self):
        self.progress_bar["value"] = 100
        self.status_label.config(text="Scan terminé!")  # Mettre à jour le label pour indiquer la fin
        self.dashboard.show_results(self.machine_info)  # Afficher les résultats sur le tableau de bord
        self.button.config(state="normal")  # Réactiver le bouton à la fin du scan

        # Calcul des statistiques
        self.total_scans += 1
        self.avg_scan_time = round(sum(self.times_per_host) / len(self.times_per_host), 2) if self.times_per_host else 0
        self.most_vulnerable_host = self.calculate_most_vulnerable_host()  # Exemple de méthode pour déterminer l'hôte vulnérable

        # Mise à jour des statistiques dans StatsPage
        self.stats_page.update_stats(self.total_scans, self.avg_scan_time, self.most_vulnerable_host)

        # Créer le dossier "resultats" s'il n'existe pas déjà
        results_folder = "resultats"
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)

        # Créer les informations à sauvegarder
        scan_data = {
            "subnet": str(self.get_subnet(self.get_local_ip())),  # Récupérer le sous-réseau
            "connected_machines": len(self.machine_info),
            "machines": []
        }

        # Collecte des informations des machines scannées
        for ip, open_ports, service_info, vulnerabilities in self.machine_info:
            machine_data = {
                "ip": ip,
                "open_ports": open_ports,
                "service_info": service_info,
                "vulnerabilities": vulnerabilities
            }
            scan_data["machines"].append(machine_data)

        # Enregistrement des résultats dans un fichier JSON
        json_file_path = os.path.join(results_folder, "scan_results.json")
        with open(json_file_path, 'w') as json_file:
            json.dump(scan_data, json_file, indent=4)

        # Créer un fichier TXT avec les adresses IP scannées
        ip_addresses = [ip for ip, _, _, _ in self.machine_info]
        txt_file_path = os.path.join(results_folder, "scanned_ips.txt")
        with open(txt_file_path, 'w') as txt_file:
            for ip in ip_addresses:
                txt_file.write(ip + "\n")

        print(f"Résultats sauvegardés dans {json_file_path} et {txt_file_path}")

    def update_dashboard(self, machine_info):
        self.machine_info = machine_info  # Stocker les résultats pour les afficher dans DashboardPage

    def get_local_ip(self):
        """
        Récupère l'adresse IP locale de la machine.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # Se connecter à une adresse publique pour déterminer l'IP locale (exemple : Google DNS)
            s.connect(('10.254.254.254', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'  # Si la connexion échoue, renvoyer l'IP localhost
        finally:
            s.close()
        return ip

    def get_subnet(self, local_ip):
        """
        Détermine le sous-réseau en fonction de l'adresse IP locale.
        """
        # Convertir l'IP locale en objet ipaddress
        ip = ipaddress.ip_address(local_ip)
        
        # Calculer le sous-réseau en supposant le masque 255.255.255.0 par défaut (mask de classe C)
        network = ipaddress.ip_network(f"{ip}/24", strict=False)
        
        return network

    def format_duration(self, elapsed_time):
        """
        Formate le temps écoulé en format lisible (minutes:secondes).
        """
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        return f"{minutes}m {seconds}s"

    def calculate_time_remaining(self, elapsed_time, scanned_count, total_count):
        """
        Calcule le temps restant estimé pour le scan en fonction du temps écoulé et du nombre de machines scannées.
        """
        if scanned_count == 0:
            return 0  # Éviter la division par zéro si aucune machine n'a été scannée

        # Calcul du temps moyen estimé par machine basé sur les derniers hôtes scannés
        average_time_per_host = sum(self.times_per_host) / len(self.times_per_host) if self.times_per_host else elapsed_time / scanned_count
        
        # Temps restant estimé pour les hôtes restants
        remaining_hosts = total_count - scanned_count
        estimated_time_remaining = remaining_hosts * average_time_per_host
        
        # Retourner le temps restant en secondes
        return round(estimated_time_remaining)

    def calculate_most_vulnerable_host(self):
        """
        Exemple de fonction pour déterminer l'hôte le plus vulnérable.
        Cette fonction peut être améliorée selon vos besoins.
        """
        # Exemple simple, retourner le premier hôte scanné (vous pouvez ajuster cette logique)
        if self.machine_info:
            return self.machine_info[0][0]  # Retourne l'IP de l'hôte le plus vulnérable
        return "Aucun"
