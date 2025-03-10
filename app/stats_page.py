import tkinter as tk
import time  # Pour mesurer le temps de scan

class StatsPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.config(bg="#2C3E50")  # Fond sombre, coherent avec HomePage et DashboardPage
        self.frame = tk.Frame(root, bg="#2C3E50")  # Fond sombre egalement pour le cadre
        self.frame.pack(fill='both', expand=True)  # Le frame prend toute la place

        # Ajouter un label pour les statistiques
        self.stats_label = tk.Label(self.frame, text="Statistiques du Scan", fg="white", bg="#2C3E50", font=("Arial", 20, "bold"))
        self.stats_label.pack(pady=30)  # Espacement pour donner de l'air autour du titre

        # Section de statistiques (Total scans, Temps moyen, Hôte vulnerable)
        self.stats_frame = tk.Frame(self.frame, bg="#2C3E50")  # Retirer la bordure autour des elements
        self.stats_frame.pack(padx=20, pady=20, fill='both', expand=True)

        self.total_scans_label = self.create_stat_label("Total de scans effectues : 0")
        self.avg_scan_time_label = self.create_stat_label("Temps moyen de scan par hôte : 0s")
        self.most_vulnerable_host_label = self.create_stat_label("Hôte le plus vulnerable : Aucun")

        # Variables pour le calcul des statistiques
        self.total_time = 0  # Temps total de tous les scans effectues
        self.scan_count = 0  # Nombre total de scans effectues
        self.hosts = {}  # Dictionnaire pour stocker les informations des hôtes (nombre de vulnerabilites ou de ports ouverts)

    def create_stat_label(self, text):
        """Cree un label stylise pour les statistiques"""
        label = tk.Label(self.stats_frame, text=text, fg="white", bg="#2C3E50", font=("Arial", 14))
        label.pack(pady=10)  # Espacement entre les informations
        return label

    def show(self):
        """Afficher la page des statistiques"""
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        """Masquer la page des statistiques"""
        self.frame.pack_forget()

    def update_stats(self, total_scans, scan_time, most_vulnerable_host):
        """Mettre à jour les statistiques affichees après chaque scan"""
        # Mise à jour du temps total et du nombre de scans
        self.total_time += scan_time
        self.scan_count += 1

        # Calcul du temps moyen de scan
        if self.scan_count > 0:
            avg_scan_time = self.total_time / self.scan_count
        else:
            avg_scan_time = 0  # Eviter la division par zero

        # Mise à jour de l'hôte le plus vulnerable
        if isinstance(most_vulnerable_host, dict):
            for host, vulnerabilities in most_vulnerable_host.items():
                if host not in self.hosts:
                    self.hosts[host] = 0
                self.hosts[host] += vulnerabilities  # Ajout du nombre de vulnerabilites pour cet hôte

            # Trouver l'hôte avec le plus grand nombre de vulnerabilites ou de ports ouverts
            most_vulnerable_host = max(self.hosts, key=self.hosts.get, default="Aucun")
        else:
            # Si on passe un seul hôte vulnerable (par exemple une chaîne), on peut l'ajouter directement
            if most_vulnerable_host not in self.hosts:
                self.hosts[most_vulnerable_host] = 0
            self.hosts[most_vulnerable_host] += 1  # Incrementer le nombre de vulnerabilites pour cet hôte

        # Mise à jour des labels avec les nouvelles valeurs
        self.total_scans_label.config(text=f"Total de scans effectues : {total_scans}")
        self.avg_scan_time_label.config(text=f"Temps moyen de scan par hôte : {avg_scan_time:.2f}s")
        self.most_vulnerable_host_label.config(text=f"Hôte le plus vulnerable : {most_vulnerable_host}")
