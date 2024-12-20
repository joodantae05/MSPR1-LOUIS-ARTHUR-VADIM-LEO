import subprocess
import platform
import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import nmap
import os
import sys

def ping(host):
    """
    Effectue un ping pour tester si l'hôte est en ligne. Utilise un délai d'attente réduit.
    """
    system_platform = platform.system().lower()

    # Choisir les arguments pour la commande ping en fonction du système d'exploitation
    if system_platform == "windows":
        cmd = ['ping', '-n', '1', '-w', '30', host]  # Réduit à 30ms
    else:
        cmd = ['ping', '-c', '1', '-W', '1', host]  # Timeout réduit à 1 seconde

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=0.5)  # Timeout global à 0.5s
        return host
    except subprocess.CalledProcessError:
        return None
    except subprocess.TimeoutExpired:
        return None


def scan_ports(host):
    """
    Scanne les ports de l'hôte en utilisant Nmap, mais en limitant les ports à ceux les plus courants.
    """
    nm = nmap.PortScanner()
    try:
        # Scanner uniquement les 100 premiers ports les plus courants (-p-1-100)
        nm.scan(hosts=host, arguments='-p 1-100 -sV --script=vuln -T4')  # Utilisation de T4 pour la rapidité
        open_ports = []
        service_info = {}
        vulnerabilities = {}

        # Si des ports ouverts sont détectés, les ajouter à la liste
        if 'tcp' in nm[host]:
            for port in nm[host]['tcp']:
                if nm[host]['tcp'][port]['state'] == 'open':
                    service = nm[host]['tcp'][port].get('name', 'Inconnu')
                    version = nm[host]['tcp'][port].get('version', 'Inconnue')
                    open_ports.append(port)
                    service_info[port] = {'service': service, 'version': version}
                    
                    # Recherche des vulnérabilités associées à ce port
                    if 'script' in nm[host]['tcp'][port]:
                        vuln_info = nm[host]['tcp'][port]['script']
                        vulnerabilities[port] = vuln_info
                    else:
                        vulnerabilities[port] = 'Aucune vulnérabilité détectée'
        
        return host, open_ports, service_info, vulnerabilities
    except Exception as e:
        print(f"Erreur lors du scan des ports pour {host}: {e}")
        # Retourner un tuple avec 4 éléments (même si c'est vide ou None en cas d'erreur)
        return host, [], {}, {}

def scan_network(network_ip):
    """
    Scanne le réseau pour trouver les hôtes en ligne avec un ping parallèle pour accélérer le processus.
    """
    network = ipaddress.ip_network(network_ip, strict=False)
    online_hosts = []
    total_ips = sum(1 for _ in network.hosts())  # Total d'IP à scanner

    # Ajuster dynamiquement le nombre de threads selon le nombre d'hôtes à scanner
    max_workers = min(100, total_ips // 10)  # Limiter le nombre de threads pour éviter une surcharge

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(ping, str(ip)): ip for ip in network.hosts()}
        for future in as_completed(futures):
            result = future.result()
            if result:
                online_hosts.append(result)

    return online_hosts, network

# Fonction pour afficher les informations sur chaque machine
def display_machine_info(ip, system_platform, system_version, open_ports, service_info, vulnerabilities):
    print(f"\n--- Informations pour la machine {ip} ---")
    print(f"Système d'exploitation: {system_platform} {system_version}")
    if open_ports:
        print(f"Ports ouverts: {', '.join(map(str, open_ports))}")
        for port in open_ports:
            service = service_info.get(port, {}).get('service', 'Inconnu')
            version = service_info.get(port, {}).get('version', 'Inconnue')
            print(f"  Port {port}: {service} {version}")
            print(f"  Vulnérabilités: {vulnerabilities.get(port, 'Aucune vulnérabilité détectée')}")
    else:
        print("Aucun port ouvert")
    print("--------------------------")
