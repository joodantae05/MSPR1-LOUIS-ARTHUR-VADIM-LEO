import subprocess
import platform

def ping(host):
    # Détecter le système d'exploitation
    system_platform = platform.system().lower()

    # Choisir les arguments pour la commande ping en fonction du système d'exploitation
    if system_platform == "windows":
        cmd = ['ping', '-n', '4', host]  # 4 pings pour Windows
    else:
        cmd = ['ping', '-c', '4', host]  # 4 pings pour Unix/Linux/Mac
    
    try:
        # Exécuter la commande ping avec Popen pour pouvoir lire la sortie en temps réel
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore') as process:
            for line in process.stdout:
                print(line, end='')  # Afficher chaque ligne du résultat de ping en temps réel

            # Attendre que le processus se termine
            process.wait()
    
    except subprocess.CalledProcessError as e:
        # Gérer l'erreur si le ping échoue (hôte non joignable)
        print(f"Erreur: Impossible de joindre l'hôte {host}. Code de retour: {e.returncode}. Détails: {e.stderr.decode(errors='ignore')}")
    except Exception as e:
        # Gestion des autres exceptions (par exemple, hôte invalide)
        print(f"Erreur: {str(e)}")

def select_ips(ip_list):
    """
    Permet à l'utilisateur de sélectionner une ou plusieurs IP à tester, ou de saisir une IP manuellement.
    """
    print("\nListe des IP disponibles :")
    for index, ip in enumerate(ip_list, start=1):
        print(f"{index}. {ip}")
    print(f"{len(ip_list) + 1}. Saisir une IP manuellement")
    print(f"{len(ip_list) + 2}. Quitter")

    # Demander à l'utilisateur de choisir les IPs à tester
    selected_indexes = input("\nEntrez les numéros des IPs à tester, séparés par des virgules (par exemple, 1,3,5), ou entrez 'q' pour quitter : ")
    
    # Si l'utilisateur veut quitter
    if selected_indexes.lower() == 'q':
        print("Vous avez choisi de quitter. Le processus est annulé.")
        return None

    # Si l'utilisateur veut saisir une IP manuellement
    if selected_indexes == str(len(ip_list) + 1):
        ip_manual = input("Entrez l'adresse IP à tester : ")
        return [ip_manual]

    try:
        # Convertir les indices sélectionnés en une liste d'IP
        selected_indexes = [int(i.strip()) - 1 for i in selected_indexes.split(',')]
        selected_ips = [ip_list[i] for i in selected_indexes]
        return selected_ips
    except (ValueError, IndexError):
        print("Entrée invalide. Assurez-vous de saisir des numéros valides.")
        return []

def ping_multiple_ips(ip_list):
    """
    Fonction qui accepte une liste d'IP et les teste une par une.
    """
    for ip in ip_list:
        print(f"Test de l'IP: {ip}")
        ping(ip)

# Lire les IP depuis le fichier './resultat/all_ips.txt' et effectuer les pings
if __name__ == "__main__":
    try:
        # Lire les IP depuis le fichier './resultat/all_ips.txt'
        with open('./resultat/all_ips.txt', 'r') as f:
            ip_dispo = [line.strip() for line in f.readlines()]

        # Demander à l'utilisateur de sélectionner les IPs à tester ou d'en saisir une manuellement
        selected_ips = select_ips(ip_dispo)
        
        # Si l'utilisateur a choisi de quitter, arrêter le processus
        if selected_ips is None:
            print("Processus annulé.")
        elif selected_ips:
            # Si l'utilisateur a sélectionné des IPs valides ou saisi une IP manuellement, effectuer les pings
            ping_multiple_ips(selected_ips)
        else:
            print("Aucune IP sélectionnée, le processus de ping est annulé.")
    
    except FileNotFoundError:
        print("Le fichier 'all_ips.txt' n'a pas été trouvé. Assurez-vous que le fichier existe.")
