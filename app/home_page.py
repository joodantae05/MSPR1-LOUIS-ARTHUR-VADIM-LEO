import socket
import ipaddress
import tkinter as tk
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
import json
import os
from datetime import datetime

from scan import scan_network, scan_ports  # Assurez-vous que scan_ports existe dans scan.py
from dashboard_page import DashboardPage
from stats_page import StatsPage

class HomePage:
    def __init__(self, root, app, dashboard, stats_page):
        self.root = root
        self.app = app
        self.dashboard = dashboard
        self.stats_page = stats_page
        self.root.config(bg="#2C3E50")  # Couleur de fond plus moderne

        # Initialisation de machine_info
        self.machine_info = []

        # Créer le cadre principal avec des coins arrondis
        self.frame = tk.Frame(root, bg="#2C3E50", bd=0)
        self.frame.pack(fill='both', expand=True, padx=30, pady=30)

        # Créer le bouton cliquable pour démarrer le scan avec un style moderne
        self.button = tk.Button(self.frame, text="Démarrer le Scan", command=self.on_click,
                                relief="flat", bd=0, font=("Segoe UI", 16), fg="white", bg="#3498DB",
                                activebackground="#2980B9", activeforeground="white", width=15, height=1,
                                highlightthickness=0, pady=8, padx=8, borderwidth=2, anchor="center")
        self.button.pack(pady=20)

        # Initialiser la barre de progression avec un style moderne
        self.progress_bar = ttk.Progressbar(self.frame, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.configure(style="TProgressbar")
        self.progress_bar.pack(pady=10)

        # Initialiser le label pour le statut avec un style moderne
        self.status_label = tk.Label(self.frame, text="", font=("Segoe UI", 12), fg="white", bg="#2C3E50")
        self.status_label.pack(pady=10)

        self.times_per_host = []  # Liste des temps de scan par hôte pour ajuster les estimations

        # Variables pour les statistiques
        self.total_scans = 0
        self.avg_scan_time = 0
        self.most_vulnerable_host = "Aucun"

        # Créer un style personnalisé pour la barre de progression
        style = ttk.Style()
        style.configure("TProgressbar",
                        thickness=20,  # Plus épaisse
                        length=400,
                        barcolor="#2ECC71")  # Couleur verte

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

    def on_click(self):
        self.button.config(state="disabled", bg="#95A5A6", activebackground="#7F8C8D")  # Désactiver et changer la couleur
        threading.Thread(target=self.start_scan).start()  # Démarrer le scan dans un thread séparé

    def start_scan(self):
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = 100
        
        # Détecter l'adresse IP locale et déterminer le sous-réseau
        local_ip = self.get_local_ip()
        subnet = self.get_subnet(local_ip)

        # Scan réseau et récupération des hôtes en ligne
        online_hosts_gen, network = scan_network(str(subnet))
        total_ips = sum(1 for _ in network.hosts())  # Nombre total d'IP à scanner
        online_hosts = list(online_hosts_gen)

        if total_ips == 0 or len(online_hosts) == 0:
            self.status_label.config(text="Aucun hôte en ligne détecté.")
            return

        # Scanner les ports des machines en ligne
        machine_info = []  # Liste pour stocker les informations des machines en ligne
        scanned_count = 0  # Compteur pour les machines scannées
        start_time = time.time()  # Commencer à chronométrer

        # Mise à jour périodique plus dynamique
        def update_periodically():
            elapsed_time = time.time() - start_time
            elapsed_time_formatted = self.format_duration(elapsed_time)

            # Mise à jour de la barre de progression et du label
            progress_percentage = (scanned_count / len(online_hosts)) * 100
            self.update_progress(progress_percentage, elapsed_time_formatted)

            if scanned_count < len(online_hosts):
                self.root.after(50, update_periodically)  # Mettre à jour toutes les 50ms

        # Lancer la mise à jour périodique
        self.root.after(50, update_periodically)

        # Traitement du scan des hôtes en ligne
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(scan_ports, ip): ip for ip in online_hosts}
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

        # Texte détaillé d'avancement
        progress_text = (
            f"Scan en cours... Durée écoulée : {elapsed_time} | "
        )

        # Mise à jour du label avec les nouvelles informations d'avancement
        self.status_label.config(text=progress_text)

    def finish_scan(self):
        self.progress_bar["value"] = 100
        self.status_label.config(text="Scan terminé !\n Fichiers JSON et TXT créés dans le dossier 'resultats'")  # Mettre à jour le label pour indiquer la fin
        self.dashboard.show_results(self.machine_info)  # Afficher les résultats sur le tableau de bord
        self.button.config(state="normal", bg="#3498DB", activebackground="#2980B9")  # Réactiver le bouton à la fin du scan

        # Calcul des statistiques
        self.total_scans += 1
        self.avg_scan_time = round(sum(self.times_per_host) / len(self.times_per_host), 2) if self.times_per_host else 0
        self.most_vulnerable_host = self.calculate_most_vulnerable_host()

        # Mise à jour des statistiques dans StatsPage
        self.stats_page.update_stats(self.total_scans, self.avg_scan_time, self.most_vulnerable_host)

        # Créer le dossier "resultats" s'il n'existe pas déjà
        results_folder = "resultats"
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)

        # Créer les informations à sauvegarder
        scan_data = {
            "scan_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "subnet": str(self.get_subnet(self.get_local_ip())),
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
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('10.254.254.254', 1))  # Se connecter à une adresse publique pour déterminer l'IP locale
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def get_subnet(self, local_ip):
        ip = ipaddress.ip_address(local_ip)
        network = ipaddress.ip_network(f"{ip}/24", strict=False)
        return network

    def format_duration(self, elapsed_time):
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        return f"{minutes}m {seconds}s"

    def calculate_most_vulnerable_host(self):
        if self.machine_info:
            return self.machine_info[0][0]  # Retourne l'IP de l'hôte le plus vulnérable
        return "Aucun"
