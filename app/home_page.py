from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
import ipaddress
import tkinter as tk
from tkinter import ttk
import threading
import requests
import time
import json
import os
from datetime import datetime
import subprocess
import re
from scan import scan_network, scan_ports
from dashboard_page import DashboardPage
from stats_page import StatsPage

class HomePage:
    def __init__(self, root, app, dashboard, stats_page):
        self.root = root
        self.app = app
        self.dashboard = dashboard
        self.stats_page = stats_page
        self.root.config(bg="#2C3E50")

        self.machine_info = []
        self.times_per_host = []
        self.total_scans = 0
        self.avg_scan_time = 0
        self.most_vulnerable_host = "Aucun"
        self.lwan = None  # Temps moyen de réponse ping

        self.frame = tk.Frame(root, bg="#2C3E50", bd=0)
        self.frame.pack(fill='both', expand=True, padx=30, pady=30)

        self.button = tk.Button(self.frame, text="Demarrer le Scan", command=self.on_click,
                                relief="flat", bd=0, font=("Segoe UI", 16), fg="white", bg="#3498DB",
                                activebackground="#2980B9", activeforeground="white", width=15, height=1)
        self.button.pack(pady=20)

        self.progress_bar = ttk.Progressbar(self.frame, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.configure(style="TProgressbar")
        self.progress_bar.pack(pady=10)

        self.status_label = tk.Label(self.frame, text="", font=("Segoe UI", 12), fg="white", bg="#2C3E50")
        self.status_label.pack(pady=10)

        style = ttk.Style()
        style.configure("TProgressbar", thickness=20, length=400, barcolor="#2ECC71")

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

    def on_click(self):
        self.button.config(state="disabled", bg="#95A5A6", activebackground="#7F8C8D")
        threading.Thread(target=self.start_scan).start()

    def start_scan(self):
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = 100
        local_ip = self.get_local_ip()
        subnet = self.get_subnet(local_ip)

        online_hosts_gen, network = scan_network(str(subnet))
        total_ips = sum(1 for _ in network.hosts())
        online_hosts = list(online_hosts_gen)

        if total_ips == 0 or len(online_hosts) == 0:
            self.status_label.config(text="Aucun hôte en ligne détecté.")
            return

        machine_info = []
        scanned_count = 0
        start_time = time.time()

        def update_periodically():
            elapsed_time = time.time() - start_time
            elapsed_time_formatted = self.format_duration(elapsed_time)
            progress_percentage = (scanned_count / len(online_hosts)) * 100
            self.update_progress(progress_percentage, elapsed_time_formatted)

            if scanned_count < len(online_hosts):
                self.root.after(50, update_periodically)

        self.root.after(50, update_periodically)

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(scan_ports, ip): ip for ip in online_hosts}
            for future in as_completed(futures):
                ip, open_ports, service_info, vulnerabilities = future.result()
                machine_info.append((ip, open_ports, service_info, vulnerabilities))

                # Calcul du temps pour chaque hôte scanné
                elapsed_time_per_host = time.time() - start_time - sum(self.times_per_host)
                self.times_per_host.append(elapsed_time_per_host)

                scanned_count += 1

        self.update_dashboard(machine_info)
        self.root.after(0, self.finish_scan)

    def update_progress(self, progress_percentage, elapsed_time):
        self.progress_bar["value"] = progress_percentage
        progress_text = f"Scan en cours... Durée écoulée : {elapsed_time}"
        self.status_label.config(text=progress_text)

    def finish_scan(self):
        self.progress_bar["value"] = 100
        self.status_label.config(text="Scan terminé !\n Fichier JSON créé dans le dossier 'resultats' et envoyé à l'API")
        self.dashboard.show_results(self.machine_info)
        self.button.config(state="normal", bg="#3498DB", activebackground="#2980B9")

        self.total_scans += 1

        # Calcul du temps moyen de scan
        if self.times_per_host:
            self.avg_scan_time = round(sum(self.times_per_host) / len(self.times_per_host), 2)
        else:
            self.avg_scan_time = 0

        self.most_vulnerable_host = self.calculate_most_vulnerable_host()

        # Mettre à jour les statistiques sur la page Stats
        self.stats_page.update_stats(self.total_scans, self.avg_scan_time, self.most_vulnerable_host)

        # Enregistrement des résultats dans un fichier JSON fusionné
        results_folder = "resultats"
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)

        # Créer un objet global pour les données
        merged_data = {
            "reseau": {
                "id_reseau": 0,  # ID du réseau, à personnaliser
                "subnet": str(self.get_subnet(self.get_local_ip())),
                "nombre_machine": len(self.machine_info),
                "date_heure": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "lwan": self.lwan if self.lwan is not None else "Inconnu",  # Temps moyen de réponse (ping)
                "id_client": 0  # ID du client, à personnaliser
            },
            "scan": {
                "id_statistique": 0,  # ID de la statistique, à personnaliser
                "nombre_scan": self.total_scans,
                "temps_moyen": self.avg_scan_time,
                "plus_vulnerable": self.most_vulnerable_host,
                "id_reseau": 0  # ID du réseau, à personnaliser
            },
            "machine": []
        }

        # Ajouter les informations sur les machines scannées
        for ip, open_ports, service_info, vulnerabilities in self.machine_info:
            machine_data = {
                "ip_adress": ip,
                "port": ', '.join(map(str, open_ports)),  # Convertir la liste de ports en une chaîne
                "service": json.dumps(service_info),  # Convertir le dictionnaire en chaîne JSON
                "vulnerabilite": json.dumps(vulnerabilities),  # Convertir le dictionnaire en chaîne JSON
                "id_reseau": 0  # ID du réseau, à personnaliser
            }
            merged_data["machine"].append(machine_data)

        # Enregistrer le fichier JSON fusionné
        json_file_path = os.path.join(results_folder, "data.json")
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(merged_data, json_file, indent=4)

        # Créer un fichier scanned_ips.txt pour les adresses IP scannées
        ip_addresses = [ip for ip, _, _, _ in self.machine_info]
        txt_file_path = os.path.join(results_folder, "scanned_ips.txt")
        with open(txt_file_path, 'w') as txt_file:
            for ip in ip_addresses:
                txt_file.write(ip + "\n")

        self.send_to_api(json_file_path)

    def send_to_api(self, json_file_path):
        """Envoie les données JSON à l'API"""
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        url = 'http://172.20.30.16:8000/scan'

        try:
            response = requests.post(url, json=data)

            if response.status_code == 200:
                print("Données envoyées avec succès !")
            else:
                print(f"Erreur lors de l'envoi des données: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de l'envoi des données à l'API: {e}")

    def update_dashboard(self, machine_info):
        self.machine_info = machine_info

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('10.254.254.254', 1))
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
            return self.machine_info[0][0]
        return "Aucun"

    def avg_time_wan(self):
        """Exécute le test de ping vers 8.8.8.8 et met à jour le fichier JSON"""
        try:
            # La commande ping diffère selon le système d'exploitation
            command = ["ping", "-c", "4", "8.8.8.8"]  # Commande pour Linux ou macOS
            # Si vous êtes sur Windows, utilisez plutôt:
            # command = ["ping", "-n", "4", "8.8.8.8"]

            # Exécution de la commande ping
            result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, universal_newlines=True)
            output, error = result.communicate()  # Récupérer à la fois la sortie et les erreurs

            # Afficher la sortie brute de ping pour voir le format
            print("Sortie brute de la commande ping :\n", output)
            print("Erreurs éventuelles de ping :\n", error)

            # Extraction du temps moyen de ping à partir de la sortie
            avg_time = self.extract_avg_time(output)

            if avg_time is None:
                print("Le temps moyen de ping n'a pas pu être extrait.")
            else:
                print(f"Temps moyen de ping extrait : {avg_time} ms")

            self.lwan = avg_time  # Stocke le temps moyen de ping
            self.update_json()  # Met à jour le fichier JSON

        except Exception as e:
            print(f"Erreur lors du test de ping: {str(e)}")

    def extract_avg_time(self, output):
        """Extrait le temps moyen du ping"""
        # Expression régulière pour Linux/macOS
        match = re.search(r"rtt min/avg/max/mdev = (\d+\.\d+)", output)
        if match:
            print(f"Temps moyen extrait pour Linux/macOS: {match.group(1)} ms")
            return match.group(1)  # Temps moyen extrait

        # Expression régulière pour Windows
        match_win = re.search(r"Average = (\d+)", output)
        if match_win:
            print(f"Temps moyen extrait pour Windows: {match_win.group(1)} ms")
            return match_win.group(1)  # Temps moyen extrait

        return None
    
    
    def update_json(self):
        """Met à jour le fichier JSON avec le temps moyen"""
        results_folder = "resultats"
        merged_data = {
            "reseau": {
                "id_reseau": 0,
                "subnet": str(self.get_subnet(self.get_local_ip())),
                "nombre_machine": len(self.machine_info),
                "date_heure": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "lwan": self.lwan if self.lwan is not None else "Inconnu",  # Mettre à jour le temps moyen
                "id_client": 0
            },
            "scan": {
                "id_statistique": 0,
                "nombre_scan": 0,
                "temps_moyen": 0,
                "plus_vulnerable": "Aucun",
                "id_reseau": 0
            },
            "machine": []
        }

        json_file_path = os.path.join(results_folder, "data.json")
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(merged_data, json_file, indent=4)
