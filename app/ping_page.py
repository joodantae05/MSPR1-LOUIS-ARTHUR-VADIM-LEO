import tkinter as tk
import subprocess
import platform
import threading
import re

class PingPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.config(bg="#2C3E50")  # Fond sombre pour toute la fenêtre
        self.frame = tk.Frame(root, bg="#2C3E50")  # Fond sombre également pour le cadre
        self.frame.pack(fill='both', expand=True)

        # Titre de la page
        self.ping_label = tk.Label(self.frame, text="Test de connectivité (Ping)", fg="white", bg="#2C3E50", font=("Arial", 20, "bold"))
        self.ping_label.pack(pady=30)  # Espacement autour du titre

        # Frame pour les champs IP (juste en dessous du titre)
        self.ip_frame = tk.Frame(self.frame, bg="#2C3E50")
        
        # Champ IP manuel
        self.ip_entry_label = tk.Label(self.ip_frame, text="Adresse IP", fg="white", bg="#2C3E50", font=("Arial", 14))
        self.ip_entry = tk.Entry(self.ip_frame, font=("Arial", 14), width=30, bg="#333344", fg="white", bd=2, relief="solid")
        
        # Sélectionner l'IP depuis un fichier
        self.ip_dropdown_label = tk.Label(self.ip_frame, text="Sélectionnez une IP à tester", fg="white", bg="#2C3E50", font=("Arial", 14))
        self.selected_ip = tk.StringVar()
        
        # Menu déroulant pour sélectionner l'IP à tester
        self.ip_dropdown = tk.OptionMenu(self.ip_frame, self.selected_ip, *self.load_ips_from_file("ips.txt"))
        self.ip_dropdown.config(width=30, font=("Arial", 14), bg="#333344", fg="white", bd=2, relief="solid", highlightthickness=0)
        
        # Ajouter les éléments à la frame
        self.ip_entry_label.pack(pady=10)
        self.ip_entry.pack(pady=10)
        self.ip_dropdown_label.pack(pady=10)
        self.ip_dropdown.pack(pady=10)

        # Placer la frame IP après le titre
        self.ip_frame.pack(pady=20)

        # Frame pour le choix de la méthode
        self.method_frame = tk.Frame(self.frame, bg="#2C2C3C", bd=5, relief="groove")
        self.method_frame.pack(padx=20, pady=20, fill='x', expand=False)

        # Choisir la méthode de test
        self.choice_label = tk.Label(self.method_frame, text="", fg="white", bg="#2C2C3C", font=("Arial", 14))
        self.choice_label.grid(row=0, column=0, padx=10, pady=10)

        self.method_var = tk.StringVar(value="manuel")
        
        # Boutons radio pour choisir la méthode
        self.manual_radio = tk.Radiobutton(self.method_frame, 
                                   text="Manuel (saisir l'adresse IP)", 
                                   variable=self.method_var, 
                                   value="manuel", 
                                   fg="white", 
                                   bg="#2C2C3C", 
                                   font=("Arial", 12), 
                                   selectcolor="#4CAF50", 
                                   activebackground="#4CAF50", 
                                   command=self.update_ui)
        self.manual_radio.grid(row=0, column=0, padx=10, pady=5, sticky="w")  # Aligner à gauche (w pour west)
        
        self.file_radio = tk.Radiobutton(self.method_frame, 
                                         text="Depuis le fichier ./resultats/scanned_ips.txt", 
                                         variable=self.method_var, 
                                         value="fichier", 
                                         fg="white", 
                                         bg="#2C2C3C", 
                                         font=("Arial", 12), 
                                         selectcolor="#4CAF50", 
                                         activebackground="#4CAF50", 
                                         command=self.update_ui)
        self.file_radio.grid(row=1, column=0, padx=10, pady=5, sticky="w")  # Aligner à gauche (w pour west)

        # Bouton pour lancer le test de ping
        self.ping_button = tk.Button(self.frame, text="Ping", command=self.run_ping,
                                relief="flat", bd=0, font=("Segoe UI", 16), fg="white", bg="#4A90E2",
                                activebackground="#357ABD", activeforeground="white", width=10, height=1,
                                highlightthickness=0, pady=8, padx=8, borderwidth=2, anchor="center")
        self.ping_button.pack(pady=20)

        # Widget pour afficher les résultats du ping, agrandi
        self.result_text = tk.Text(self.frame, height=15, width=70, font=("Arial", 12), bg="#333344", fg="white", wrap="word")
        self.result_text.pack(pady=10, padx=20)  # Ajout de padding horizontal

        # Initialiser l'interface en fonction du choix
        self.update_ui()

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
            widget.pack_forget()

        if method == "manuel":
            # Afficher le champ pour saisir l'adresse IP
            self.ip_entry_label.pack(pady=10)
            self.ip_entry.pack(pady=10)
        else:
            # Afficher le champ pour sélectionner une IP depuis un fichier
            self.ip_dropdown_label.pack(pady=10)
            self.ip_dropdown.pack(pady=10)

    def run_ping(self):
        """Exécuter le test de ping dans un thread pour éviter le blocage de l'interface"""
        ip = self.ip_entry.get() if self.method_var.get() == "manuel" else self.selected_ip.get()

        if ip:
            # Effacer les anciennes entrées avant de commencer un nouveau test
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
            result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, universal_newlines=True, encoding="iso-8859-1")

            # Lire les sorties ligne par ligne et les afficher en temps réel
            for line in result.stdout:
                line = self.clean_ping_output(line)  # Nettoyer les caractères indésirables
                self.root.after(0, self.update_result, f"{line.strip()}\n")

            result.wait()  # Attendre que la commande de ping soit terminée

            # Vérification du code de retour pour savoir si le ping a réussi
            if result.returncode != 0:
                self.root.after(0, self.update_result, f"Ping échoué pour {ip}: Erreur lors de l'exécution")
            else:
                self.root.after(0, self.update_result, f"Ping terminé pour {ip}")

        except Exception as e:
            # Gestion des erreurs et mise à jour des résultats
            self.root.after(0, self.update_result, f"Erreur pour l'IP {ip}: {str(e)}")

    def clean_ping_output(self, line):
        """Nettoyer la sortie de la commande ping pour supprimer les caractères indésirables"""
        # Nettoyer les caractères indésirables tout en gardant les caractères valides
        line = re.sub(r'[^\x20-\x7E]', ' ', line)  # Remplacer les caractères de contrôle (non imprimables) par un espace
        return line

    def update_result(self, result):
        """Met à jour le widget Text avec le résultat du ping"""
        self.result_text.insert(tk.END, result)
        self.result_text.yview(tk.END)  # Scroll down to the last line

    def load_ips_from_file(self, filename):
        """Charger les IPs depuis un fichier texte"""
        try:
            # Vérification de l'existence du fichier
            with open('./resultats/scanned_ips.txt', "r") as file:
                ip_list = [line.strip() for line in file.readlines() if line.strip()]
                return ip_list
        except FileNotFoundError:
            self.update_result("Le fichier 'scanned_ips.txt' n'a pas été trouvé.")
            return []  # Retourner une liste vide si le fichier n'existe pas
