import tkinter as tk

class PingPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.config(bg="#1E1E2D")  # Fond sombre, cohérent avec HomePage et DashboardPage
        self.frame = tk.Frame(root, bg="#1E1E2D")  # Fond sombre également pour le cadre

        # Ajouter un label pour la page de ping
        self.ping_label = tk.Label(self.frame, text="Test de connectivité (Ping)", fg="white", bg="#1E1E2D", font=("Arial", 18, "bold"))
        self.ping_label.pack(pady=30)  # Espacement pour donner de l'air autour du titre

        # Ajouter un label pour l'adresse IP ou le domaine à tester (initialement vide)
        self.ip_label = tk.Label(self.frame, text="Adresse IP ou domaine: (Ex: 8.8.8.8)", fg="white", bg="#1E1E2D", font=("Arial", 14))
        self.ip_label.pack(pady=10)

        # Champ de saisie pour l'adresse IP ou domaine
        self.ip_entry = tk.Entry(self.frame, font=("Arial", 14), width=30, bg="#333344", fg="white", bd=2, relief="solid")
        self.ip_entry.pack(pady=10)

        # Bouton pour lancer le test de ping
        self.ping_button = tk.Button(self.frame, text="Lancer le Test Ping", command=self.run_ping, font=("Arial", 14), fg="white", bg="#4CAF50", activebackground="#45a049", width=20, height=2)
        self.ping_button.pack(pady=20)

        # Label pour afficher les résultats du test ping
        self.result_label = tk.Label(self.frame, text="Résultat: Aucun test effectué", fg="white", bg="#1E1E2D", font=("Arial", 14))
        self.result_label.pack(pady=20)

    def show(self):
        """Afficher la page Ping"""
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        """Masquer la page Ping"""
        self.frame.pack_forget()

    def run_ping(self):
        """Exécuter le test de ping"""
        ip = self.ip_entry.get()  # Récupérer l'IP ou domaine entré par l'utilisateur
        if ip:
            # Pour la simulation, nous allons afficher un message de réussite ou d'échec
            # Dans un cas réel, vous intégreriez ici un appel à une fonction de ping réseau
            result = self.simulate_ping(ip)
            self.result_label.config(text=f"Résultat: {result}")
        else:
            self.result_label.config(text="Veuillez entrer une adresse IP ou un domaine.")

    def simulate_ping(self, ip):
        """Simuler un résultat de ping"""
        # Cette fonction simule un ping en renvoyant un succès ou un échec
        # Dans une vraie application, vous utiliseriez la bibliothèque `ping` ou `subprocess` pour effectuer le ping
        if ip == "8.8.8.8":
            return "Ping réussi"
        else:
            return "Échec du ping"
