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
    Effectue un ping pour tester si l'hôte est en ligne, avec un délai réduit.
    """
    system_platform = platform.system().lower()

    # Utiliser des arguments optimisés pour le ping en fonction du système
    cmd = []
    if system_platform == "windows":
        cmd = ['ping', '-n', '1', '-w', '30', host]  # Réduit à 30ms pour windows
    else:
        cmd = ['ping', '-c', '1', '-W', '1', host]  # Timeout réduit à 1 seconde pour Linux/MacOS

    try:
        # Diminuer le timeout global pour accélérer
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=0.5)
        return host
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None


def scan_ports(host):
    """
    Scanne les ports de l'hôte en utilisant Nmap pour les ports les plus courants.
    Utilisation de l'option '-sV' pour obtenir des informations détaillées sur les services.
    """
    nm = nmap.PortScanner()
    try:
        # Utilisation de la plage 1-1024 pour couvrir plus de ports populaires tout en augmentant la vitesse
        # Ne pas inclure l'option -O pour éviter de scanner l'OS
        nm.scan(hosts=host, arguments='-p 1-1024 -sV --script=vuln -T4')  # -T4 pour la rapidité

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

                    # Recherche des vulnérabilités associées au port
                    vuln_info = nm[host]['tcp'][port].get('script', 'Aucune vulnérabilité détectée')
                    vulnerabilities[port] = vuln_info

        # Ne pas récupérer l'OS, donc on ne retourne plus `os_info`
        return host, open_ports, service_info, vulnerabilities

    except nmap.nmap.PortScannerError as e:
        print(f"Erreur lors du scan Nmap pour {host}: {e}")
        return host, [], {}, {}
    except Exception as e:
        print(f"Erreur lors du scan des ports pour {host}: {e}")
        return host, [], {}, {}


def scan_network(network_ip):
    """
    Scanne le réseau pour trouver les hôtes en ligne en utilisant des threads pour accélérer le processus.
    """
    network = ipaddress.ip_network(network_ip, strict=False)
    online_hosts = []
    total_ips = sum(1 for _ in network.hosts())  # Total d'IP à scanner

    # Dynamiser le nombre de threads en fonction du nombre d'hôtes à scanner
    max_workers = min(100, total_ips // 10)  # Limiter les threads pour éviter la surcharge

    # Utiliser ThreadPoolExecutor pour ping parallèle
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(ping, str(ip)): ip for ip in network.hosts()}
        for future in as_completed(futures):
            result = future.result()
            if result:
                online_hosts.append(result)

    return online_hosts, network


def display_machine_info(ip, open_ports, service_info, vulnerabilities):
    """
    Affiche les informations détaillées sur chaque machine, optimisé pour un affichage rapide.
    """
    print(f"\n--- Informations pour la machine {ip} ---")
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


def optimized_scan(network_ip):
    """
    Effectue un scan optimisé du réseau avec un nombre accru de threads et des plages de ports élargies.
    """
    online_hosts, network = scan_network(network_ip)
    
    # Utilisation de ThreadPoolExecutor pour scanner les ports en parallèle sur chaque hôte trouvé
    with ThreadPoolExecutor(max_workers=20) as executor:  # Utilisation de plus de threads pour le scan des ports
        futures = {executor.submit(scan_ports, host): host for host in online_hosts}
        
        for future in as_completed(futures):
            host, open_ports, service_info, vulnerabilities = future.result()
            display_machine_info(host, open_ports, service_info, vulnerabilities)
