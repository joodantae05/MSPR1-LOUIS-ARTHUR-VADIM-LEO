import tkinter as tk
import time  # Pour mesurer le temps de scan

class StatsPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.config(bg="#2C3E50")  # Fond sombre, cohérent avec HomePage et DashboardPage
        self.frame = tk.Frame(root, bg="#2C3E50")  # Fond sombre également pour le cadre
        self.frame.pack(fill='both', expand=True)  # Le frame prend toute la place

        # Ajouter un label pour les statistiques
        self.stats_label = tk.Label(self.frame, text="Statistiques du Scan", fg="white", bg="#2C3E50", font=("Arial", 20, "bold"))
        self.stats_label.pack(pady=30)  # Espacement pour donner de l'air autour du titre

        # Section de statistiques (Total scans, Temps moyen, Hôte vulnérable)
        self.stats_frame = tk.Frame(self.frame, bg="#2C3E50", bd=5, relief="groove")
        self.stats_frame.pack(padx=20, pady=20, fill='both', expand=True)

        self.total_scans_label = self.create_stat_label("Total de scans effectués: 0")
        self.avg_scan_time_label = self.create_stat_label("Temps moyen de scan: 0s")
        self.most_vulnerable_host_label = self.create_stat_label("Hôte le plus vulnérable: Aucun")

        # Variables pour le calcul des statistiques
        self.total_time = 0  # Temps total de tous les scans effectués
        self.scan_count = 0  # Nombre total de scans effectués
        self.hosts = {}  # Dictionnaire pour stocker les informations des hôtes (nombre de vulnérabilités ou de ports ouverts)

    def create_stat_label(self, text):
        """Crée un label stylisé pour les statistiques"""
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
        """Mettre à jour les statistiques affichées après chaque scan"""
        # Mise à jour du temps total et du nombre de scans
        self.total_time += scan_time
        self.scan_count += 1
    
        # Calcul du temps moyen de scan
        if self.scan_count == 1:
            # Lors du premier scan, le temps moyen est égal au temps du scan
            avg_scan_time = scan_time
        else:
            # Pour les scans suivants, le temps moyen est le temps total divisé par le nombre de scans
            avg_scan_time = self.total_time / self.scan_count
    
        # Mise à jour de l'hôte le plus vulnérable
        if isinstance(most_vulnerable_host, dict):
            for host, vulnerabilities in most_vulnerable_host.items():
                if host not in self.hosts:
                    self.hosts[host] = 0
                self.hosts[host] += vulnerabilities  # Ajout du nombre de vulnérabilités pour cet hôte
    
            # Trouver l'hôte avec le plus grand nombre de vulnérabilités ou de ports ouverts
            most_vulnerable_host = max(self.hosts, key=self.hosts.get, default="Aucun")
        else:
            # Si on passe un seul hôte vulnérable (par exemple une chaîne), on peut l'ajouter directement
            if most_vulnerable_host not in self.hosts:
                self.hosts[most_vulnerable_host] = 0
            self.hosts[most_vulnerable_host] += 1  # Incrémenter le nombre de vulnérabilités pour cet hôte
    
        # Mise à jour des labels avec les nouvelles valeurs
        self.total_scans_label.config(text=f"Total de scans effectués: {total_scans}")
        self.avg_scan_time_label.config(text=f"Temps moyen de scan: {avg_scan_time:.2f}s")
        self.most_vulnerable_host_label.config(text=f"Hôte le plus vulnérable: {most_vulnerable_host}")
