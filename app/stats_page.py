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
        self.most_vulnerable_host = "Aucun"  # Par défaut, pas d'hôte vulnérable

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

    def update_stats(self, total_scans, avg_scan_time, most_vulnerable_host):
        """Mettre à jour les statistiques affichées après chaque scan"""
        self.total_scans_label.config(text=f"Total de scans effectués: {total_scans}")
        self.avg_scan_time_label.config(text=f"Temps moyen de scan: {avg_scan_time:.2f}s")
        self.most_vulnerable_host_label.config(text=f"Hôte le plus vulnérable: {most_vulnerable_host}")