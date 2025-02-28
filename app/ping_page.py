import tkinter as tk
import subprocess
import platform
import threading
import re

class PingPage:
    def __init__(self, root, app):
        """Initialisation de la page de test de connectivité (Ping)"""
        self.root = root
        self.app = app
        self.root.config(bg="#2C3E50")  # Fond sombre pour toute la fenêtre
        self.frame = tk.Frame(root, bg="#2C3E50")  # Fond sombre pour le cadre
        self.frame.pack(fill='both', expand=True, padx=30, pady=30)

        # Titre de la page
        self.ping_label = tk.Label(self.frame, text="Test de connectivité (Ping)", fg="white", bg="#2C3E50", font=("Arial", 20, "bold"))
        self.ping_label.pack(pady=10)

        # Frame pour l'adresse IP
        self.ip_frame = tk.Frame(self.frame, bg="#2C3E50")
        # Champ IP manuel
        self.ip_entry_label = tk.Label(self.ip_frame, text="Adresse IP", fg="white", bg="#2C3E50", font=("Arial", 14))
        self.ip_entry = tk.Entry(self.ip_frame, font=("Arial", 14), width=30, bg="#333344", fg="white", bd=2, relief="solid")
        
        # Ajouter les éléments à la frame
        self.ip_entry_label.grid(row=0, column=0, pady=5, padx=5)
        self.ip_entry.grid(row=0, column=1, pady=10, padx=5)
        
        # Placer la frame IP après le titre
        self.ip_frame.pack(pady=20)

        # Frame pour le choix de la méthode et le bouton de ping
        self.method_ping_frame = tk.Frame(self.frame, bg="#2C3E50")
        self.method_ping_frame.pack(pady=10, fill="x", expand=True)

        # Frame pour le choix de la méthode
        self.method_frame = tk.Frame(self.method_ping_frame, bg="#2C2C3C", bd=5, relief="groove")
        self.method_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Choisir la méthode de test
        self.choice_label = tk.Label(self.method_frame, text="Choisir la méthode de test", fg="white", bg="#2C2C3C", font=("Arial", 14))
        self.choice_label.grid(row=0, column=0, padx=10, pady=10)

        self.method_var = tk.StringVar(value="manuel")  # Initialiser avec la méthode manuelle
        
        # Boutons radio pour choisir la méthode
        self.manual_radio = tk.Radiobutton(self.method_frame, 
                                           text="Manuel", 
                                           variable=self.method_var, 
                                           value="manuel", 
                                           fg="white", 
                                           bg="#2C2C3C", 
                                           font=("Arial", 12), 
                                           selectcolor="#4CAF50", 
                                           activebackground="#4CAF50", 
                                           command=self.update_ui)
        self.manual_radio.grid(row=1, column=0, padx=10, pady=5, sticky="w")  # Aligner à gauche
        
        self.file_radio = tk.Radiobutton(self.method_frame, 
                                         text="Depuis un fichier de résultats", 
                                         variable=self.method_var, 
                                         value="fichier", 
                                         fg="white", 
                                         bg="#2C2C3C", 
                                         font=("Arial", 12), 
                                         selectcolor="#4CAF50", 
                                         activebackground="#4CAF50", 
                                         command=self.update_ui)
        self.file_radio.grid(row=2, column=0, padx=10, pady=5, sticky="w")  # Aligner à gauche

        # Bouton pour lancer le test de ping
        self.ping_button = tk.Button(self.method_ping_frame, text="Lancer le Ping", command=self.run_ping,
                                     relief="flat", bd=0, font=("Segoe UI", 16), fg="white", bg="#4A90E2",
                                     activebackground="#357ABD", activeforeground="white", width=15, height=1,
                                     highlightthickness=0, pady=8, padx=8, borderwidth=2, anchor="center")
        self.ping_button.grid(row=0, column=1, padx=10)

        # Widget pour afficher les résultats du ping
        self.result_text = tk.Text(self.method_ping_frame, height=10, width=50, font=("Arial", 12), bg="#333344", fg="white", wrap="word", state=tk.DISABLED)
        self.result_text.grid(row=0, column=2, padx=10, pady=10)

        # Frame pour sélectionner l'IP à partir du fichier
        self.ip_dropdown_frame = tk.Frame(self.frame, bg="#2C3E50")
        self.ip_dropdown_frame.pack(pady=10, fill="x", expand=True)
        
        # Sélectionner une IP depuis un fichier
        self.selected_ip = tk.StringVar()
        self.ip_dropdown = tk.OptionMenu(self.ip_dropdown_frame, self.selected_ip, "")
        self.ip_dropdown.config(width=30, font=("Arial", 14), bg="#333344", fg="white", bd=2, relief="solid", highlightthickness=0)
        self.ip_dropdown.pack(pady=10)

        # Initialiser l'interface en fonction du choix
        self.update_ui()

        # Mettre à jour les IPs toutes les 10 secondes
        self.update_ips()

    def show(self):
        """Afficher la page Ping"""
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        """Masquer la page Ping"""
        self.frame.pack_forget()

    def update_ui(self):
        """Met à jour l'interface en fonction de la méthode choisie"""
        method = self.method_var.get()

        # Réinitialiser la frame IP avant de reconfigurer
        for widget in self.ip_frame.winfo_children():
            widget.grid_forget()

        if method == "manuel":
            # Afficher le champ pour saisir l'adresse IP
            self.ip_entry_label.grid(row=0, column=0, pady=5, padx=5)
            self.ip_entry.grid(row=0, column=1, pady=10, padx=5)
            self.ip_dropdown_frame.pack_forget()
        else:
            # Afficher le champ pour sélectionner une IP depuis un fichier
            self.ip_dropdown_frame.pack(pady=10, fill="x", expand=True)
            self.ip_entry.grid_forget()

    def run_ping(self):
        """Exécuter le test de ping dans un thread pour éviter le blocage de l'interface"""
        ip = self.ip_entry.get() if self.method_var.get() == "manuel" else self.selected_ip.get()

        if ip:
            # Désactiver le bouton pour éviter de lancer plusieurs pings
            self.ping_button.config(state=tk.DISABLED)

            # Effacer les anciennes entrées avant de commencer un nouveau test
            self.result_text.config(state=tk.NORMAL)  # Permet de modifier le contenu
            self.result_text.delete(1.0, tk.END)  # Effacer le contenu du widget Text

            # Utiliser un thread pour exécuter la commande de ping sans bloquer l'interface
            thread = threading.Thread(target=self.execute_ping, args=(ip,))
            thread.start()
        else:
            self.update_result("Veuillez entrer une adresse IP ou en sélectionner une.")

    def execute_ping(self, ip):
        """Exécuter un véritable test de ping via subprocess et afficher un retour simplifié"""
        try:
            # Déterminer la commande de ping en fonction du système d'exploitation
            system = platform.system().lower()
            if system == "windows":
                command = ["ping", "-n", "3", ip]
            else:
                command = ["ping", "-c", "3", ip]
    
            # Utiliser l'encodage ISO-8859-1 pour Windows ou autre système avec des caractères spéciaux
            result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, universal_newlines=True, encoding="utf-16")
    
            # Lire les sorties ligne par ligne et les afficher en temps réel
            for line in result.stdout:
                line = self.clean_ping_output(line)  # Nettoyer les caractères indésirables
                self.root.after(0, self.update_result, f"{line.strip()}\n")  # Mise à jour en temps réel
    
            result.wait()  # Attendre que la commande de ping soit terminée
    
            # Vérification du code de retour pour savoir si le ping a réussi
            if result.returncode != 0:
                self.root.after(0, self.update_result, f"Ping échoué pour {ip}: Erreur lors de l'exécution\n")
            else:
                self.root.after(0, self.update_result, f"Ping terminé pour {ip}\n")
    
        except Exception as e:
            # Capture des erreurs potentielles et affichage dans le widget Text
            error_message = f"Erreur pour l'IP {ip}: {str(e)}"
            self.root.after(0, self.update_result, error_message)
    
        # Réactiver le bouton une fois que le test est terminé
        self.root.after(0, self.ping_button.config, {'state': tk.NORMAL})

    def clean_ping_output(self, line):
        """Nettoyer la sortie de la commande ping pour supprimer les caractères indésirables"""
        # Nettoyer les caractères indésirables tout en gardant les caractères valides
        line = re.sub(r'[^\x20-\x7E]', ' ', line)  # Remplacer les caractères de contrôle (non imprimables) par un espace
        return line

    def update_result(self, result):
        """Met à jour le widget Text avec le résultat du ping"""
        self.result_text.config(state=tk.NORMAL)  # Assurer que le widget Text est modifiable
        self.result_text.insert(tk.END, result)   # Ajouter le texte
        self.result_text.yview(tk.END)            # Faire défiler vers le bas
        self.result_text.config(state=tk.DISABLED)  # Rendre le widget Text non modifiable après mise à jour

    def load_ips_from_file(self, filename):
        """Charger les IPs depuis un fichier texte"""
        try:
            # Vérification de l'existence du fichier
            with open(filename, "r") as file:
                ip_list = [line.strip() for line in file.readlines() if line.strip()]
                return ip_list
        except FileNotFoundError:
            self.update_result("Le fichier 'scanned_ips.txt' n'a pas été trouvé.")
            return []  # Retourner une liste vide si le fichier n'existe pas
    
    def update_ips(self):
        """Met à jour la liste des IPs depuis le fichier toutes les 10 secondes"""
        ip_list = self.load_ips_from_file("resultats/scanned_ips.txt")
        
        # Mettre à jour le menu déroulant
        if ip_list:
            menu = self.ip_dropdown["menu"]
            menu.delete(0, "end")
            for ip in ip_list:
                menu.add_command(label=ip, command=tk._setit(self.selected_ip, ip))
        
        # Planifier la prochaine mise à jour dans 10 secondes
        self.root.after(10000, self.update_ips)
