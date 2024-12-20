import tkinter as tk
import subprocess
import platform
import threading

class PingPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.config(bg="#1E1E2D")  # Fond sombre
        self.frame = tk.Frame(root, bg="#1E1E2D")  # Fond sombre également pour le cadre

        # Ajouter un label pour la page de ping
        self.ping_label = tk.Label(self.frame, text="Test de connectivité (Ping)", fg="white", bg="#1E1E2D", font=("Arial", 18, "bold"))
        self.ping_label.pack(pady=30)  # Espacement pour donner de l'air autour du titre

        # Ajouter une option pour choisir la méthode de ping
        self.choice_label = tk.Label(self.frame, text="Choisissez une méthode pour le test de ping :", fg="white", bg="#1E1E2D", font=("Arial", 14))
        self.choice_label.pack(pady=10)

        # Créer des boutons radio pour choisir entre IP manuelle ou depuis un fichier
        self.method_var = tk.StringVar(value="manuel")
        
        self.method_frame = tk.Frame(self.frame, bg="#1E1E2D")
        
        self.manual_radio = tk.Radiobutton(self.method_frame, text="Manuel (saisir l'adresse IP)", variable=self.method_var, value="manuel", fg="white", bg="#1E1E2D", font=("Arial", 12), selectcolor="#4CAF50", activebackground="#4CAF50", command=self.update_ui)
        self.manual_radio.grid(row=0, column=0, padx=10, pady=5)

        self.file_radio = tk.Radiobutton(self.method_frame, text="Depuis un fichier", variable=self.method_var, value="fichier", fg="white", bg="#1E1E2D", font=("Arial", 12), selectcolor="#4CAF50", activebackground="#4CAF50", command=self.update_ui)
        self.file_radio.grid(row=1, column=0, padx=10, pady=5)
        
        self.method_frame.pack(pady=10)

        # Champ de saisie pour l'adresse IP (visible si l'option manuelle est sélectionnée)
        self.ip_entry_label = tk.Label(self.frame, text="Adresse IP", fg="white", bg="#1E1E2D", font=("Arial", 14))
        self.ip_entry = tk.Entry(self.frame, font=("Arial", 14), width=30, bg="#333344", fg="white", bd=2, relief="solid")

        # Liste déroulante des IPs lues depuis le fichier (visible si l'option fichier est sélectionnée)
        self.ip_dropdown_label = tk.Label(self.frame, text="Sélectionnez une IP à tester", fg="white", bg="#1E1E2D", font=("Arial", 14))
        self.selected_ip = tk.StringVar()
        self.ip_dropdown = tk.OptionMenu(self.frame, self.selected_ip, "")

        # Bouton pour lancer le test de ping
        self.ping_button = tk.Button(self.frame, text="Lancer le Test Ping", command=self.run_ping, font=("Arial", 14), fg="white", bg="#4CAF50", activebackground="#45a049", width=20, height=2)
        self.ping_button.pack(pady=20)

        # Ajouter un widget Text pour afficher les résultats du ping
        self.result_text = tk.Text(self.frame, height=5, width=50, font=("Arial", 12), bg="#333344", fg="white", wrap="word")
        self.result_text.pack(pady=10)

        # Charger les IPs depuis un fichier
        self.ip_list = self.load_ips_from_file("ips.txt")
        if self.ip_list:
            self.selected_ip.set(self.ip_list[0])  # Définir une IP par défaut si le fichier n'est pas vide

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
        if method == "manuel":
            self.ip_entry_label.pack(pady=10)
            self.ip_entry.pack(pady=10)
            self.ip_dropdown_label.pack_forget()
            self.ip_dropdown.pack_forget()
        else:
            self.ip_entry_label.pack_forget()
            self.ip_entry.pack_forget()
            self.ip_dropdown_label.pack(pady=10)
            self.ip_dropdown.pack(pady=10)

    def run_ping(self):
        """Exécuter le test de ping dans un thread pour éviter le blocage de l'interface"""
        ip = self.ip_entry.get() if self.method_var.get() == "manuel" else self.selected_ip.get()

        if ip:
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
    
            # Exécuter la commande de ping
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, universal_newlines=True)
    
            # Vérifier si la commande a échoué
            if result.returncode != 0:
                error_message = result.stderr
                self.update_result(f"Ping échoué : {error_message.strip()}")
                return
    
            # Décoder la sortie (stdout)
            output = result.stdout
            formatted_output = []
    
            # Analyser la sortie en fonction du système
            if system == "windows":
                # Format spécifique pour Windows
                for line in output.splitlines():
                    if "bytes from" in line:
                        parts = line.split()
                        time = parts[6]  # Le temps en ms est dans la 7ème position
                        formatted_output.append(f"Ping réussi: Temps={time}")
                    elif "Request Timed Out" in line:
                        formatted_output.append("Ping échoué : Demande expirée")
            else:
                # Format pour les systèmes Unix (Linux, macOS)
                for line in output.splitlines():
                    if "bytes from" in line:
                        parts = line.split()
                        time = parts[6].split("=")[1]  # Temps en ms après "time="
                        formatted_output.append(f"Ping réussi: Temps={time} ms")
                    elif "Request timeout" in line:
                        formatted_output.append("Ping échoué : Demande expirée")
    
            if not formatted_output:
                formatted_output.append("Ping échoué : Aucune réponse reçue")
    
            # Mettre à jour le texte dans le widget Text sur le thread principal
            self.root.after(0, self.update_result, "\n".join(formatted_output))
    
        except Exception as e:
            # Gestion des erreurs et mise à jour des résultats
            self.root.after(0, self.update_result, f"Erreur: {str(e)}")

    def update_result(self, result):
        """Met à jour le widget Text avec le résultat du ping"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

    def load_ips_from_file(self, filename):
        """Charger les IPs depuis un fichier texte"""
        try:
            with open(filename, "r") as file:
                ip_list = [line.strip() for line in file.readlines() if line.strip()]
                return ip_list
        except FileNotFoundError:
            self.update_result("Fichier non trouvé")
            return []
