import tkinter as tk
import socket
import platform
import time  # Import pour gérer l'heure

# Fonction pour obtenir l'adresse IP locale
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IPv4, Datagramme (envoi de message sans connexion)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))  # Utilisation d'une adresse distante non routable pour obtenir l'IP locale
        ip = s.getsockname()[0]  # Retourne l'adresse IP de l'interface locale
    except Exception:
        ip = '127.0.0.1'  # En cas d'échec, retourne l'IP de loopback
    finally:
        s.close()
    return ip

# Fonction pour obtenir les informations du système
def get_system_info():
    try:
        # Récupérer le nom de la machine (nom d'hôte)
        vm_name = platform.node()
        
        # Récupérer le système d'exploitation
        os_name = platform.system()
        
        # Récupérer la version du système d'exploitation
        os_version = platform.release()
        
        # Organiser toutes les informations dans un dictionnaire
        system_info = {
            "Nom de la machine": vm_name,
            "Système d'exploitation": os_name,
            "Version du système d'exploitation": os_version,
        }
        return system_info
    except Exception as e:
        # Gérer les erreurs potentielles
        return {"Erreur": str(e)}

# Création de l'interface graphique avec Tkinter
class DashboardPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.config(bg="#1E1E2D")  # Fond sombre

        # Créer un cadre principal pour la mise en page à deux colonnes
        self.main_frame = tk.Frame(root, bg="#1E1E2D")
        self.main_frame.pack(fill='both', expand=True, padx=40, pady=40)  # Ajouter de l'espace autour du cadre principal

        # Créer un cadre pour la section de gauche (Scan)
        self.left_frame = tk.Frame(self.main_frame, bg="#1E1E2D")
        self.left_frame.pack(side="left", fill="y", padx=20, pady=20, expand=True)

        # Créer un cadre pour la section de droite (Informations système)
        self.right_frame = tk.Frame(self.main_frame, bg="#1E1E2D")
        self.right_frame.pack(side="right", fill="y", padx=20, pady=20, expand=True)

        # Créer un cadre pour centrer le titre des résultats du scan dans la section gauche
        self.left_title_frame = tk.Frame(self.left_frame, bg="#1E1E2D")
        self.left_title_frame.pack(fill="x", pady=10)  # Remplir toute la largeur et ajouter un peu d'espace

        # Ajouter un label centré pour le titre des résultats du scan
        self.result_label = tk.Label(self.left_title_frame, text="Résultats du dernier scan", fg="white", bg="#1E1E2D", font=("Arial", 18, "bold"))
        self.result_label.pack(anchor="center", padx=10, pady=20)  # Centré avec un peu d'espace

        # Créer un cadre pour centrer le titre des informations système dans la section droite
        self.right_title_frame = tk.Frame(self.right_frame, bg="#1E1E2D")
        self.right_title_frame.pack(fill="x", pady=10)  # Remplir toute la largeur et ajouter un peu d'espace

        # Ajouter un label centré pour le titre des informations système
        self.info_label = tk.Label(self.right_title_frame, text="Informations Système", fg="white", bg="#1E1E2D", font=("Arial", 18, "bold"))
        self.info_label.pack(anchor="center", padx=10, pady=20)  # Centré avec un peu d'espace

        # Créer un bouton pour rafraîchir les informations système
        self.refresh_button = tk.Button(self.right_frame, text="Rafraîchir Infos Système", command=self.refresh_system_info,
                                relief="flat", bd=0, font=("Arial", 16), fg="white", bg="#4A90E2",
                                activebackground="#357ABD", activeforeground="white", width=20, height=2,
                                highlightthickness=0, pady=10)

        # Initialiser les informations système et l'adresse IP locale
        self.system_info = get_system_info()
        self.local_ip = get_local_ip()

        # Initialiser la section des résultats du scan
        self.scan_results_frame = tk.Frame(self.left_frame, bg="#1E1E2D", height=400)  # Augmenter la taille du cadre
        self.scan_results_frame.pack(fill="both", padx=20, pady=20, expand=True)  # Section des résultats du scan

        # Ajouter une barre de défilement pour la liste des IPs scannées
        self.scrollbar = tk.Scrollbar(self.scan_results_frame)
        self.scrollbar.pack(side="right", fill="y")

        # Créer un canvas pour le défilement
        self.canvas = tk.Canvas(self.scan_results_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Créer un cadre dans le canvas pour contenir les résultats
        self.results_frame = tk.Frame(self.canvas, bg="#1E1E2D")
        self.canvas.create_window((0, 0), window=self.results_frame, anchor="nw")

        # Configurer la barre de défilement
        self.scrollbar.config(command=self.canvas.yview)

        # Afficher les informations système et l'adresse IP locale
        self.display_system_info()

    def show(self):
        """Afficher la page du tableau de bord"""
        self.main_frame.pack(fill='both', expand=True)

    def hide(self):
        """Cacher la page du tableau de bord"""
        self.main_frame.pack_forget()

    def display_system_info(self):
        """Afficher les informations système locales"""
        # Vider la section droite avant de réafficher les nouvelles informations
        for widget in self.right_frame.winfo_children():
            widget.pack_forget()

        # Réafficher le titre et le bouton de rafraîchissement
        self.right_title_frame.pack(fill="x", pady=10)
        self.refresh_button.pack(pady=20)

        # Affichage des informations système dans la section droite
        for key, value in self.system_info.items():
            label = tk.Label(self.right_frame, text=f"{key}: {value}", fg="white", bg="#1E1E2D", font=("Arial", 12))
            label.pack(anchor="w", pady=5, padx=20)  # Alignement à gauche avec un peu d'espace à gauche

        # Affichage de l'adresse IP locale
        ip_label = tk.Label(self.right_frame, text=f"Adresse IP locale: {self.local_ip}", fg="white", bg="#1E1E2D", font=("Arial", 12))
        ip_label.pack(anchor="w", pady=5, padx=20)  # Alignement à gauche avec un peu d'espace à gauche

        # Affichage de l'OS local
        os_label = tk.Label(self.right_frame, text="OS: {} {}".format(
            self.system_info.get("Système d'exploitation", "Inconnu"),
            self.system_info.get("Version du système d'exploitation", "Inconnue")
        ), fg="white", bg="#1E1E2D", font=("Arial", 12))
        os_label.pack(anchor="w", pady=5, padx=20)  # Alignement à gauche avec un peu d'espace à gauche

    def refresh_system_info(self):
        """Rafraîchir les informations système et l'adresse IP locale"""
        self.system_info = get_system_info()  # Récupérer à nouveau les informations système
        self.local_ip = get_local_ip()  # Récupérer à nouveau l'adresse IP locale
        self.display_system_info()  # Mettre à jour l'affichage avec les nouvelles informations

    def show_results(self, machine_info):
        result_text = f"Scan effectué à {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"  # Ajouter la date et l'heure

        for machine in machine_info:
            # Vérifier si le tuple contient bien 4 éléments (sans l'OS)
            if len(machine) == 4:  # (host, open_ports, service_info, vulnerabilities)
                ip, open_ports, service_info, vulnerabilities = machine
            else:
                continue  # Si le tuple a un nombre incorrect d'éléments, passer à la machine suivante

            # Convertir chaque élément de 'vulnerabilities' en chaîne avant de les joindre
            vulnerabilities_str = self.format_vulnerabilities(vulnerabilities)

            # Ajouter l'IP dans un label avec une taille de police plus petite
            ip_label = tk.Label(self.results_frame, text=f"IP: {self.format_ip(ip)}", fg="white", bg="#1E1E2D", font=("Arial", 10))
            ip_label.pack(anchor="w", padx=10, pady=5)

            ports_label = tk.Label(self.results_frame, text=f"Ports ouverts: {self.format_ports(open_ports)}", fg="white", bg="#1E1E2D", font=("Arial", 10))
            ports_label.pack(anchor="w", padx=10, pady=5)

            services_label = tk.Label(self.results_frame, text=f"Services détectés: {self.format_services(service_info)}", fg="white", bg="#1E1E2D", font=("Arial", 10))
            services_label.pack(anchor="w", padx=10, pady=5)

            vuln_label = tk.Label(self.results_frame, text=f"Vulnérabilités: {vulnerabilities_str}", fg="white", bg="#1E1E2D", font=("Arial", 10))
            vuln_label.pack(anchor="w", padx=10, pady=5)

        # Mettre à jour le canvas après ajout des widgets
        self.results_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def format_vulnerabilities(self, vulnerabilities):
        """Formatage des vulnérabilités pour un affichage lisible"""
        if isinstance(vulnerabilities, dict):
            # Si les vulnérabilités sont sous forme de dictionnaire, on les affiche sous forme de clé: valeur
            vuln_list = [f"{key}: {vuln}" for key, vuln in vulnerabilities.items()]
            return '\n'.join(vuln_list) if vuln_list else "Aucune vulnérabilité détectée"
        elif isinstance(vulnerabilities, list):
            # Si les vulnérabilités sont sous forme de liste, on les joint
            return ', '.join(vulnerabilities) if vulnerabilities else "Aucune vulnérabilité détectée"
        else:
            # Cas par défaut si les vulnérabilités ne sont ni une liste ni un dictionnaire
            return "Aucune vulnérabilité détectée"

    def format_ip(self, ip):
        """Formatage de l'IP pour une meilleure lisibilité"""
        return f"[ {ip} ]"  # Encadrer l'IP avec des crochets pour plus de clarté

    def format_ports(self, ports):
        """Formatage des ports ouverts avec un texte stylisé"""
        return ', '.join([f"Port {port}" for port in ports]) if ports else "Aucun port ouvert"

    def format_services(self, services):
        """Formatage des services avec un texte stylisé"""
        return '\n'.join([f"Service: {service['service']} (Version: {service['version']})" 
                          for service in services.values()]) if services else "Aucun service détecté"
