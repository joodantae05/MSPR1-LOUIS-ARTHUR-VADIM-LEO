import tkinter as tk
import socket
import platform
import time
from tkinter import messagebox

# Fonction pour obtenir l'adresse IP locale
def get_local_ip():
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

# Fonction pour obtenir les informations du système
def get_system_info():
    try:
        vm_name = platform.node()
        os_name = platform.system()
        os_version = platform.release()

        system_info = {
            "Nom de la machine": vm_name,
            "Système d'exploitation": os_name,
            "Version du système d'exploitation": os_version,
        }
        return system_info
    except Exception as e:
        return {"Erreur": str(e)}


# Création de l'interface graphique avec Tkinter
class DashboardPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.config(bg="#2C3E50")

        self.main_frame = tk.Frame(root, bg="#2C3E50")
        self.main_frame.pack(fill='both', expand=True, padx=40, pady=40)

        self.left_frame = tk.Frame(self.main_frame, bg="#2C3E50")
        self.left_frame.pack(side="left", fill="y", padx=20, pady=20, expand=True)

        self.right_frame = tk.Frame(self.main_frame, bg="#2C3E50")
        self.right_frame.pack(side="right", fill="y", padx=20, pady=20, expand=True)

        self.left_title_frame = tk.Frame(self.left_frame, bg="#2C3E50")
        self.left_title_frame.pack(fill="x", pady=10)

        self.result_label = tk.Label(self.left_title_frame, text="Résultats du dernier scan", fg="white", bg="#2C3E50", font=("Arial", 18, "bold"))
        self.result_label.pack(anchor="center", padx=10, pady=20)

        self.right_title_frame = tk.Frame(self.right_frame, bg="#2C3E50")
        self.right_title_frame.pack(fill="x", pady=10)

        self.info_label = tk.Label(self.right_title_frame, text="Informations Système", fg="white", bg="#2C3E50", font=("Arial", 18, "bold"))
        self.info_label.pack(anchor="center", padx=10, pady=20)

        self.refresh_button = tk.Button(self.right_frame, text="Reset Infos Système", command=self.refresh_system_info,
                                relief="flat", bd=0, font=("Segoe UI", 16), fg="white", bg="#4A90E2",
                                activebackground="#357ABD", activeforeground="white", width=20, height=1,
                                highlightthickness=0, pady=8, padx=8, borderwidth=2, anchor="center")

        self.system_info = get_system_info()
        self.local_ip = get_local_ip()

        self.scan_results_frame = tk.Frame(self.left_frame, bg="#1E1E2D", height=600)
        self.scan_results_frame.pack(fill="both", padx=20, pady=20, expand=True)

        self.scrollbar = tk.Scrollbar(self.scan_results_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas = tk.Canvas(self.scan_results_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.results_frame = tk.Frame(self.canvas, bg="#1E1E2D")
        self.canvas.create_window((0, 0), window=self.results_frame, anchor="nw")

        self.scrollbar.config(command=self.canvas.yview)

        self.display_system_info()

    def show(self):
        self.main_frame.pack(fill='both', expand=True)

    def hide(self):
        self.main_frame.pack_forget()

    def display_system_info(self):
        for widget in self.right_frame.winfo_children():
            widget.pack_forget()

        self.right_title_frame.pack(fill="x", pady=10)
        self.refresh_button.pack(pady=20)

        # Affichage des informations système
        for key, value in self.system_info.items():
            label = tk.Label(self.right_frame, text=f"{key}: {value}", fg="white", bg="#2C3E50", font=("Arial", 12))
            label.pack(anchor="w", pady=5, padx=20)

        ip_label = tk.Label(self.right_frame, text=f"Adresse IP locale: {self.local_ip}", fg="white", bg="#2C3E50", font=("Arial", 12))
        ip_label.pack(anchor="w", pady=5, padx=20)

        os_label = tk.Label(self.right_frame, text="OS: {} {}".format(
            self.system_info.get("Système d'exploitation", "Inconnu"),
            self.system_info.get("Version du système d'exploitation", "Inconnue")
        ), fg="white", bg="#2C3E50", font=("Arial", 12))
        os_label.pack(anchor="w", pady=5, padx=20)


    def refresh_system_info(self):
        self.system_info = get_system_info()
        self.local_ip = get_local_ip()
        self.display_system_info()

    def show_results(self, machine_info):
        result_text = f"Scan effectué à {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        for machine in machine_info:
            if len(machine) == 4:
                ip, open_ports, service_info, vulnerabilities = machine
            else:
                continue

            vulnerabilities_str = self.format_vulnerabilities(vulnerabilities)

            ip_label = tk.Label(self.results_frame, text=f"IP : {self.format_ip(ip)}", fg="white", bg="#1E1E2D", font=("Arial", 10), wraplength=350)
            ip_label.pack(anchor="w", padx=20, pady=5)

            ports_label = tk.Label(self.results_frame, text=f"Ports ouverts: {self.format_ports(open_ports)}", fg="white", bg="#1E1E2D", font=("Arial", 10), wraplength=350)
            ports_label.pack(anchor="w", padx=20, pady=5)

            services_label = tk.Label(self.results_frame, text=f"Services détectés: {self.format_services(service_info)}", fg="white", bg="#1E1E2D", font=("Arial", 10), wraplength=350)
            services_label.pack(anchor="w", padx=20, pady=5)

            vuln_label = tk.Label(self.results_frame, text=f"Vulnérabilités: {vulnerabilities_str}", fg="white", bg="#1E1E2D", font=("Arial", 10), wraplength=350)
            vuln_label.pack(anchor="w", padx=20, pady=5)

        self.results_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def format_vulnerabilities(self, vulnerabilities):
        if isinstance(vulnerabilities, dict):
            vuln_list = [f"{key}: {vuln}" for key, vuln in vulnerabilities.items()]
            return '\n'.join(vuln_list) if vuln_list else "Aucune vulnérabilité détectée"
        elif isinstance(vulnerabilities, list):
            return ', '.join(vulnerabilities) if vulnerabilities else "Aucune vulnérabilité détectée"
        else:
            return "Aucune vulnérabilité détectée"

    def format_ip(self, ip):
        return f"{ip}"

    def format_ports(self, ports):
        return ', '.join([f"Port {port}" for port in ports]) if ports else "Aucun port ouvert"

    def format_services(self, services):
        return '\n'.join([f"Service: {service['service']} (Version: {service['version']})" 
                          for service in services.values()]) if services else "Aucun service détecté"
