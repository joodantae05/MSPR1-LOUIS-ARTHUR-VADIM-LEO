import socket
import ipaddress
import threading
import scapy.all as scapy

def get_local_network():
    """Récupère le sous-réseau de l'IP locale de la machine"""
    local_ip = socket.gethostbyname(socket.gethostname())
    local_network = ipaddress.IPv4Network(f'{local_ip}/24', strict=False)
    return local_network

def scan_network(network_ip, update_progress):
    """Scan du réseau local avec ARP"""
    active_ips = []
    local_network = ipaddress.IPv4Network(network_ip, strict=False)
    hosts = list(local_network.hosts())

    def scan_ip(ip):
        """Scanne une adresse IP avec ARP"""
        ans, _ = scapy.arping(str(ip), timeout=1, verbose=False)
        if ans:
            active_ips.append(str(ip))
        update_progress(len(active_ips) / len(hosts))

    threads = []
    for ip in hosts:
        thread = threading.Thread(target=scan_ip, args=(ip,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return active_ips
