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
    # Détecter le système d'exploitation
    system_platform = platform.system().lower()

    # Choisir les arguments pour la commande ping en fonction du système d'exploitation
    if system_platform == "windows":
        cmd = ['ping', '-n', '1', '-w', '50', host]  # '-w' pour limiter le temps d'attente (50ms)
    else:
        cmd = ['ping', '-c', '1', '-W', '1', host]  # '-W' pour définir un délai d'attente plus court

    try:
        # Exécuter la commande ping et vérifier la réponse
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=1)
        return host
    except subprocess.CalledProcessError:
        return None
    except subprocess.TimeoutExpired:
        return None

def scan_ports(host):
    # Créer une instance de scanner Nmap
    nm = nmap.PortScanner()

    try:
        # Scanner les ports et obtenir la version des services (-sV) et vérifier les vulnérabilités (--script=vuln)
        nm.scan(hosts=host, arguments='-p 1-1024 -sV --script=vuln -T4')
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
        return host, [], {}, {}

def get_system_info(host):
    """
    Récupère les informations du système d'exploitation et de la version pour l'hôte local.
    """
    try:
        # On utilise la machine locale pour obtenir ces infos (si la machine est distante, une connexion SSH serait nécessaire)
        system_platform = platform.system()
        system_version = platform.version()
        
        # Retourne les informations du système
        return system_platform, system_version
    except Exception as e:
        return None, None

def scan_network(network_ip):
    # Scanner un réseau IP en envoyant des pings
    network = ipaddress.ip_network(network_ip, strict=False)
    online_hosts = []
    total_ips = sum(1 for _ in network.hosts())  # Total d'IP à scanner

    # Utiliser ThreadPoolExecutor pour effectuer des pings en parallèle
    with ThreadPoolExecutor(max_workers=100) as executor:  # Augmenter les threads à 100
        # Soumettre les tâches de ping pour chaque IP dans le sous-réseau
        futures = {executor.submit(ping, str(ip)): ip for ip in network.hosts()}
        
        # Parcourir les résultats avec une barre de progression
        for i, future in enumerate(as_completed(futures), start=1):
            ip = future.result()
            if ip:  # Si l'IP est en ligne
                online_hosts.append(ip)
            # Mise à jour de la barre de progression
            sys.stdout.write(f"\rScan réseau : {i}/{total_ips} ({(i / total_ips) * 100:.2f}%)")
            sys.stdout.flush()

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

# Obtenez l'adresse IP locale de votre machine de manière plus fiable
local_ip = socket.gethostbyname(socket.gethostname())

# Trouver l'adresse du sous-réseau en utilisant la partie réseau de l'adresse IP locale
network_ip = '.'.join(local_ip.split('.')[:-1]) + '.0/24'

# Créer le dossier 'resultat' si il n'existe pas
output_dir = "resultat"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Scanner le réseau
start_time = time.time()
ip_dispo, network = scan_network(network_ip)
end_time = time.time()

# Afficher les informations de sous-réseau et le nombre total de machines connectées
print(f"\nSous-réseau scanné: {network_ip}")
print(f"Nombre total de machines connectées: {len(ip_dispo)}")

# Stocker les IP des machines connectées et leurs informations systèmes
machine_info = []

# Scanner les ports de toutes les machines en ligne sans barre de progression
with ThreadPoolExecutor(max_workers=10) as executor:  # Utilisation de threads pour le scan de ports
    futures = {executor.submit(scan_ports, ip): ip for ip in ip_dispo}
    
    # Parcourir les résultats avec une barre de progression
    for i, future in enumerate(as_completed(futures), start=1):
        ip, open_ports, service_info, vulnerabilities = future.result()

        # Récupérer les informations système de la machine
        system_platform, system_version = get_system_info(ip)

        # Ajouter l'IP, les informations système, les ports ouverts, les versions de services et vulnérabilités à la liste
        machine_info.append((ip, system_platform, system_version, open_ports, service_info, vulnerabilities))

        # Afficher les informations de la machine dans la console
        display_machine_info(ip, system_platform, system_version, open_ports, service_info, vulnerabilities)

        # Mise à jour de la barre de progression pour le scan des ports
        sys.stdout.write(f"\rScan des ports : {i}/{len(ip_dispo)} ({(i / len(ip_dispo)) * 100:.2f}%)")
        sys.stdout.flush()

# Calcul du pourcentage du scan du réseau
total_ips_count = len(list(network.hosts()))  # Nombre total d'IP à scanner
reachable_ips_count = len(ip_dispo)  # Nombre d'IP qui ont répondu au ping
network_percentage = (reachable_ips_count / total_ips_count) * 100 if total_ips_count > 0 else 0

# Calcul du pourcentage du scan des ports
machines_with_open_ports = sum(1 for _, _, _, open_ports, _, _ in machine_info if open_ports)
port_scan_percentage = (machines_with_open_ports / len(machine_info)) * 100 if len(machine_info) > 0 else 0

# Générer un nom unique pour le fichier de scan
timestamp = time.strftime('%Y%m%d_%H%M%S')
file_path = os.path.join(output_dir, f'last_scan.txt')

# Créer le fichier pour ce scan avec un nom unique
with open(file_path, 'w', encoding='utf-8') as f:
    # Écrire la date de création
    f.write(f"Date de création du fichier : {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Ajouter le nombre total de machines
    f.write(f"\nTotal de machines connectées: {len(machine_info)}\n")
    
    # Enregistrer les informations de chaque machine dans le fichier
    for ip, system_platform, system_version, open_ports, service_info, vulnerabilities in machine_info:
        f.write(f"IP: {ip}\n")
        f.write(f"  Système d'exploitation: {system_platform} {system_version}\n")
        f.write(f"  Ports ouverts: {', '.join(map(str, open_ports)) if open_ports else 'Aucun port ouvert'}\n")
        for port in open_ports:
            service = service_info.get(port, {}).get('service', 'Inconnu')
            version = service_info.get(port, {}).get('version', 'Inconnue')
            f.write(f"    Port {port}: {service} {version}\n")
            f.write(f"    Vulnérabilités: {vulnerabilities.get(port, 'Aucune vulnérabilité détectée')}\n")
        f.write("\n")

# Afficher le nombre total de machines connectées dans la console
print(f"\nTotal de machines connectées: {len(machine_info)}")

print(f"Les informations du dernier scan ont été sauvegardées dans '{file_path}'.")

# Ouvrir le fichier 'all_ips.txt' en mode 'w' pour écraser les informations précédentes
all_ips_file = os.path.join(output_dir, 'all_ips.txt')

# Créer ou écraser le fichier 'all_ips.txt' et y écrire les nouvelles IPs
with open(all_ips_file, 'w', encoding='utf-8') as f:
    for ip in ip_dispo:
        f.write(ip + '\n')

print(f"Les adresses IP ont été ajoutées à '{all_ips_file}'.")
