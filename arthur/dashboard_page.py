import tkinter as tk
import platform
import socket
import psutil
from datetime import datetime

class DashboardPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.config(bg="#1E1E2D")  # Fond sombre, similaire à HomePage
        
        # Créer le cadre principal pour le tableau de bord
        self.frame = tk.Frame(root, bg="#1E1E2D")
        self.frame.pack(fill='both', expand=True)  # Le frame prend toute la place

        # Ajouter un label pour afficher les résultats du scan
        self.result_label = tk.Label(self.frame, text="Résultats du dernier scan", fg="white", bg="#1E1E2D", font=("Arial", 18, "bold"))
        self.result_label.pack(pady=30)  # Espacement pour bien séparer l'élément du haut
        
        # Ajouter un label pour l'heure et la date du scan (initialement vide)
        self.scan_time_label = tk.Label(self.frame, text="", fg="white", bg="#1E1E2D", font=("Arial", 12))
        self.scan_time_label.pack(pady=10, anchor="center")  # Centrer le label
        
        # Ajouter un label pour afficher les informations de la machine locale
        self.machine_info_label = tk.Label(self.frame, text="Informations sur la machine locale", fg="white", bg="#1E1E2D", font=("Arial", 18, "bold"))
        self.machine_info_label.pack(pady=30)

    def show(self):
        """Afficher la page du tableau de bord"""
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        """Cacher la page du tableau de bord"""
        self.frame.pack_forget()

    def show_results(self, machine_info):
        """Afficher les résultats du scan"""
        # Récupérer l'heure et la date du lancement du scan
        scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Mettre à jour le label avec l'heure du scan
        self.scan_time_label.config(text=f"Lancé le: {scan_time}")
        
        # Afficher le total de machines connectées
        total_machines = len(machine_info)
        total_label = tk.Label(self.frame, text=f"Total de machines connectées: {total_machines}", fg="white", bg="#1E1E2D", font=("Arial", 14))
        total_label.pack(pady=10, anchor="center")  # Centrer le label

        # Afficher les informations de chaque machine scannée
        for ip, open_ports, service_info, vulnerabilities in machine_info:
            if isinstance(ip, tuple):
                ip = ', '.join(ip)  # Convertir les tuples en chaîne d'IP

            # Affichage de l'adresse IP de la machine
            ip_label = tk.Label(self.frame, text=f"IP: {ip}", fg="white", bg="#1E1E2D", font=("Arial", 14, "bold"))
            ip_label.pack(anchor="center", pady=5)  # Centrer le label

            # Affichage du système d'exploitation de la machine
            os_label = tk.Label(self.frame, text=f"Système d'exploitation: {service_info.get('os', 'Inconnu')}", fg="white", bg="#1E1E2D", font=("Arial", 12))
            os_label.pack(anchor="center", pady=5)  # Centrer le label

            # Affichage des ports ouverts ou aucun port ouvert
            if not open_ports:
                no_ports_label = tk.Label(self.frame, text="  Aucun port ouvert", fg="#FF6F61", bg="#1E1E2D", font=("Arial", 12))
                no_ports_label.pack(anchor="center", pady=5)  # Centrer le label
            else:
                for port in open_ports:
                    self.display_port_details(port, service_info, vulnerabilities)

    def display_port_details(self, port, service_info, vulnerabilities):
        """Afficher les détails des ports ouverts"""
        service = service_info.get(port, {}).get('service', 'Inconnu')
        version = service_info.get(port, {}).get('version', 'Inconnue')
        vulnerabilities_text = vulnerabilities.get(port, 'Aucune vulnérabilité détectée')

        # Affichage du port ouvert
        port_label = tk.Label(self.frame, text=f"    Port {port}: {service} {version}", fg="white", bg="#1E1E2D", font=("Arial", 12))
        port_label.pack(anchor="center", pady=5)  # Centrer le label

        # Affichage des vulnérabilités associées au port
        vuln_label = tk.Label(self.frame, text=f"    Vulnérabilités: {vulnerabilities_text}", fg="#FF6F61", bg="#1E1E2D", font=("Arial", 12))
        vuln_label.pack(anchor="center", pady=5)  # Centrer le label

    def display_ip(self, ip, service_info):
        """Afficher les informations liées à une IP"""
        ip_label = tk.Label(self.frame, text=f"IP: {ip}", fg="white", bg="#1E1E2D", font=("Arial", 14, "bold"))
        ip_label.pack(anchor="center", pady=5)  # Centrer le label

        os_label = tk.Label(self.frame, text=f"Système d'exploitation: {service_info.get('os', 'Inconnu')}", fg="white", bg="#1E1E2D", font=("Arial", 12))
        os_label.pack(anchor="center", pady=5)  # Centrer le label

    def display_ports(self, open_ports, service_info, vulnerabilities):
        """Afficher les informations sur les ports ouverts"""
        if open_ports:
            ports_label = tk.Label(self.frame, text=f"Ports ouverts: {', '.join(map(str, open_ports))}", fg="white", bg="#1E1E2D", font=("Arial", 12))
            ports_label.pack(anchor="center", pady=5)  # Centrer le label

            for port in open_ports:
                self.display_port_details(port, service_info, vulnerabilities)

    def get_local_machine_info(self):
        """Récupérer les informations de la machine locale"""
        try:
            # Nom de la machine
            machine_name = platform.node()

            # Système d'exploitation
            os_name = platform.system()
            os_version = platform.version()

            # Adresse IP locale
            ip_address = socket.gethostbyname(socket.gethostname())

            # Informations sur les sous-réseaux
            network_info = psutil.net_if_addrs()
            subnets = {interface: [addr.address for addr in addresses if addr.family == psutil.AF_INET] for interface, addresses in network_info.items()}

            # Affichage des informations
            self.display_machine_info(machine_name, os_name, os_version, ip_address, subnets)
        except Exception as e:
            print(f"Erreur lors de la récupération des informations système: {e}")

    def display_machine_info(self, machine_name, os_name, os_version, ip_address, subnets):
        """Afficher les informations de la machine locale dans le tableau de bord"""
        machine_name_label = tk.Label(self.frame, text=f"Nom de la machine: {machine_name}", fg="white", bg="#1E1E2D", font=("Arial", 12))
        machine_name_label.pack(anchor="w", padx=20, pady=5)

        os_label = tk.Label(self.frame, text=f"Système d'exploitation: {os_name} {os_version}", fg="white", bg="#1E1E2D", font=("Arial", 12))
        os_label.pack(anchor="w", padx=20, pady=5)

        ip_label = tk.Label(self.frame, text=f"Adresse IP: {ip_address}", fg="white", bg="#1E1E2D", font=("Arial", 12))
        ip_label.pack(anchor="w", padx=20, pady=5)

        for interface, addresses in subnets.items():
            subnets_label = tk.Label(self.frame, text=f"Interface {interface} - Sous-réseau(s): {', '.join(addresses)}", fg="white", bg="#1E1E2D", font=("Arial", 12))
            subnets_label.pack(anchor="w", padx=20, pady=5)

