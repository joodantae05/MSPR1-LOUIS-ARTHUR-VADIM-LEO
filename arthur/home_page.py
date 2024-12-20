import tkinter as tk
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess
import platform
import ipaddress
import socket
import nmap
import time
import sys
import os

# Fonctions de scan (copiées depuis scan.py)
def ping(host):
    system_platform = platform.system().lower()
    if system_platform == "windows":
        cmd = ['ping', '-n', '1', '-w', '50', host]
    else:
        cmd = ['ping', '-c', '1', '-W', '1', host]

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=1)
        return host
    except subprocess.CalledProcessError:
        return None
    except subprocess.TimeoutExpired:
        return None

def scan_ports(host):
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=host, arguments='-p 1-1024 -sV --script=vuln -T4')
        open_ports = []
        service_info = {}
        vulnerabilities = {}

        if 'tcp' in nm[host]:
            for port in nm[host]['tcp']:
                if nm[host]['tcp'][port]['state'] == 'open':
                    service = nm[host]['tcp'][port].get('name', 'Inconnu')
                    version = nm[host]['tcp'][port].get('version', 'Inconnue')
                    open_ports.append(port)
                    service_info[port] = {'service': service, 'version': version}
                    if 'script' in nm[host]['tcp'][port]:
                        vuln_info = nm[host]['tcp'][port]['script']
                        vulnerabilities[port] = vuln_info
                    else:
                        vulnerabilities[port] = 'Aucune vulnérabilité détectée'

        return host, open_ports, service_info, vulnerabilities
    except Exception as e:
        print(f"Erreur lors du scan des ports pour {host}: {e}")
        return host, [], {}, {}

def scan_network():
    # Obtenir l'IP locale et détecter automatiquement le sous-réseau
    local_ip = socket.gethostbyname(socket.gethostname())
    network_ip = '.'.join(local_ip.split('.')[:-1]) + '.0/24'  # Génère automatiquement le sous-réseau à scanner
    network = ipaddress.ip_network(network_ip, strict=False)

    online_hosts = []
    total_ips = sum(1 for _ in network.hosts())

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(ping, str(ip)): ip for ip in network.hosts()}

        for i, future in enumerate(as_completed(futures), start=1):
            ip = future.result()
            if ip:
                online_hosts.append(ip)
            sys.stdout.write(f"\rScan réseau : {i}/{total_ips} ({(i / total_ips) * 100:.2f}%)")
            sys.stdout.flush()

    return online_hosts, network

class HomePage:
    def __init__(self, root, app, dashboard):
        self.root = root
        self.app = app
        self.dashboard = dashboard
        self.root.config(bg="#141526")
        self.frame = tk.Frame(root, bg="#141526")

        # Créer le bouton cliquable
        self.button = tk.Button(self.frame, text="Scan du réseau", command=self.on_click,
                                relief="solid", bd=3, font=("Arial", 16), fg="white", bg="#333344",
                                activebackground="#444455", activeforeground="white", highlightthickness=2,
                                highlightbackground="white", width=20, height=2)
        self.button.pack(pady=20)

        # Animation d'effet de vague
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

        # Initialiser la barre de progression (cachée au début)
        self.progress_bar = ttk.Progressbar(self.frame, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)
        self.progress_bar.place_forget()

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

    def on_click(self):
        self.start_scan()

    def on_enter(self, event):
        self.button.config(highlightcolor="#555566", highlightthickness=4)

    def on_leave(self, event):
        self.button.config(highlightcolor="white", highlightthickness=2)

    def start_scan(self):
        self.progress_bar.place(relx=0.5, rely=0.6, anchor="center")
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = 100
        self.perform_scan()

    def perform_scan(self):
        online_hosts, network = scan_network()

        machine_info = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(scan_ports, ip): ip for ip in online_hosts}
            for i, future in enumerate(as_completed(futures), start=1):
                ip, open_ports, service_info, vulnerabilities = future.result()

                # Ajout des résultats dans une structure pour le Dashboard
                machine_info.append((ip, open_ports, service_info, vulnerabilities))

                sys.stdout.write(f"\rScan des ports : {i}/{len(online_hosts)} ({(i / len(online_hosts)) * 100:.2f}%)")
                sys.stdout.flush()

        self.update_dashboard(machine_info)

    def update_dashboard(self, machine_info):
        # Cette méthode met à jour le Dashboard avec les résultats du scan
        self.dashboard.show_results(machine_info)
        self.progress_bar.place_forget()
