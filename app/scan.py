import subprocess
import platform
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
import nmap
import time

def ping(host):
    """
    Effectue un ping pour tester si l'hôte est en ligne avec un delai reduit.
    """
    system_platform = platform.system().lower()

    # Utiliser des arguments optimises pour le ping en fonction du système
    cmd = []
    if system_platform == "windows":
        cmd = ['ping', '-n', '1', '-w', '30', host]  # Reduit à 30ms pour windows
    else:
        cmd = ['ping', '-c', '1', '-W', '1', host]  # Timeout reduit à 1 seconde pour Linux/MacOS

    try:
        # Timeout reduit à 0.3 seconde pour accelerer le ping
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=0.3)
        return host
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None


def scan_ports(host):
    """
    Scanne les ports de l'hôte en utilisant Nmap pour les ports les plus courants.
    Utilisation de l'option '-sV' pour obtenir des informations detaillees sur les services.
    """
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=host, arguments=' -sV -T4')  # Utilisation de T4 pour la rapidite

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

                    # Recherche des vulnerabilites associees au port
                    vuln_info = nm[host]['tcp'][port].get('script', 'Aucune vulnerabilite detectee')
                    vulnerabilities[port] = vuln_info

        return host, open_ports, service_info, vulnerabilities

    except nmap.nmap.PortScannerError as e:
        print(f"Erreur lors du scan Nmap pour {host}: {e}")
        return host, [], {}, {}
    except Exception as e:
        print(f"Erreur lors du scan des ports pour {host}: {e}")
        return host, [], {}, {}


def scan_network(network_ip):
    """
    Scanne le reseau pour trouver les hôtes en ligne en utilisant des threads pour accelerer le processus.
    """
    network = ipaddress.ip_network(network_ip, strict=False)
    online_hosts = []
    total_ips = sum(1 for _ in network.hosts())  # Total d'IP à scanner

    # Dynamiser le nombre de threads en fonction du nombre d'hôtes à scanner
    max_workers = min(50, total_ips // 10)  # Limiter les threads à 50 pour eviter une surcharge

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(ping, str(ip)): ip for ip in network.hosts()}
        for future in as_completed(futures):
            result = future.result()
            if result:
                online_hosts.append(result)

    return online_hosts, network


def display_machine_info(ip, open_ports, service_info, vulnerabilities):
    """
    Affiche les informations detaillees sur chaque machine, optimise pour un affichage rapide.
    """
    print(f"\n--- Informations pour la machine {ip} ---")
    if open_ports:
        print(f"Ports ouverts: {', '.join(map(str, open_ports))}")
        for port in open_ports:
            service = service_info.get(port, {}).get('service', 'Inconnu')
            version = service_info.get(port, {}).get('version', 'Inconnue')
            print(f"  Port {port}: {service} {version}")
            print(f"  Vulnerabilites: {vulnerabilities.get(port, 'Aucune vulnerabilite detectee')}")
    else:
        print("Aucun port ouvert")
    print("--------------------------")
