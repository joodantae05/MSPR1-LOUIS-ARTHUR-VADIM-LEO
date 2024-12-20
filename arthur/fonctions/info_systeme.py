import socket
import platform

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

# Appeler la fonction pour obtenir les informations système
system_info = get_system_info()

# Affichage des informations système
print("Informations systèmes : ")
for key, value in system_info.items():
    print(f"{key}: {value}")

# Appeler la fonction pour obtenir l'adresse IP locale
ip_local = get_local_ip()
print(f"Adresse IP locale : {ip_local}"'\n')
