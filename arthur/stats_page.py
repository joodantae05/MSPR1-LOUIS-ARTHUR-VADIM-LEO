import tkinter as tk

class StatsPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.config(bg="#1E1E2D")  # Fond sombre, cohérent avec HomePage et DashboardPage
        self.frame = tk.Frame(root, bg="#1E1E2D")  # Fond sombre également pour le cadre

        # Ajouter un label pour les statistiques
        self.stats_label = tk.Label(self.frame, text="Statistiques du Scan", fg="white", bg="#1E1E2D", font=("Arial", 18, "bold"))
        self.stats_label.pack(pady=30)  # Espacement pour donner de l'air autour du titre
        
        # Ajouter un label pour les statistiques de scan (données fictives ici pour exemple)
        self.total_scans_label = tk.Label(self.frame, text="Total de scans effectués: 0", fg="white", bg="#1E1E2D", font=("Arial", 14))
        self.total_scans_label.pack(pady=10)  # Espacement entre les informations

        self.avg_scan_time_label = tk.Label(self.frame, text="Temps moyen de scan: 0s", fg="white", bg="#1E1E2D", font=("Arial", 14))
        self.avg_scan_time_label.pack(pady=10)

        self.most_vulnerable_host_label = tk.Label(self.frame, text="Hôte le plus vulnérable: Aucun", fg="white", bg="#1E1E2D", font=("Arial", 14))
        self.most_vulnerable_host_label.pack(pady=10)

    def show(self):
        """Afficher la page des statistiques"""
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        """Masquer la page des statistiques"""
        self.frame.pack_forget()

    def update_stats(self, total_scans, avg_scan_time, most_vulnerable_host):
        """Mettre à jour les statistiques affichées"""
        self.total_scans_label.config(text=f"Total de scans effectués: {total_scans}")
        self.avg_scan_time_label.config(text=f"Temps moyen de scan: {avg_scan_time}s")
        self.most_vulnerable_host_label.config(text=f"Hôte le plus vulnérable: {most_vulnerable_host}")
