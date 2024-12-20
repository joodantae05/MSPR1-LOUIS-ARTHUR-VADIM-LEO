import tkinter as tk
import time  # Pour mesurer le temps de scan

class StatsPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.config(bg="#1E1E2D")  # Fond sombre, cohérent avec HomePage et DashboardPage
        self.frame = tk.Frame(root, bg="#1E1E2D")  # Fond sombre également pour le cadre
        self.frame.pack(fill='both', expand=True)  # Le frame prend toute la place

        # Ajouter un label pour les statistiques
        self.stats_label = tk.Label(self.frame, text="Statistiques du Scan", fg="white", bg="#1E1E2D", font=("Arial", 20, "bold"))
        self.stats_label.pack(pady=30)  # Espacement pour donner de l'air autour du titre

        # Section de statistiques (Total scans, Temps moyen, Hôte vulnérable)
        self.stats_frame = tk.Frame(self.frame, bg="#2C2C3C", bd=5, relief="groove")
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
        label = tk.Label(self.stats_frame, text=text, fg="white", bg="#2C2C3C", font=("Arial", 14))
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

    def scan(self):
        """Simuler un scan et mettre à jour les statistiques"""
        start_time = time.time()  # Enregistrer le début du scan
        
        # Simulation de scan (remplacez ceci par la logique réelle de scan)
        time.sleep(2)  # Exemple : simuler un scan de 2 secondes
        
        end_time = time.time()  # Fin du scan
        scan_time = end_time - start_time  # Temps écoulé pour ce scan

        # Exemple de détection d'un hôte vulnérable (remplacez ceci par votre logique de détection réelle)
        vulnerable_host = "192.168.1.100"  # Par exemple, un hôte vulnérable trouvé
        
        # Mettre à jour les statistiques après ce scan
        self.scan_count += 1
        self.total_time += scan_time
        avg_scan_time = self.total_time / self.scan_count
        self.update_stats(self.scan_count, avg_scan_time, vulnerable_host)

        # Animer la mise à jour (par exemple, changement de couleur du label)
        self.animate_update()

    def animate_update(self):
        """Ajouter une animation simple sur la mise à jour"""
        # Change temporairement la couleur de fond pour attirer l'attention
        self.stats_frame.config(bg="#FF6F61")  # Changer la couleur de fond de la section

        # Rétablir la couleur après un court délai (500ms)
        self.root.after(500, lambda: self.stats_frame.config(bg="#2C2C3C"))

# Exemple d'utilisation de StatsPage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dashboard des Statistiques de Scan")
    root.geometry("600x500")  # Taille de la fenêtre

    # Ajout de bords et de coins arrondis à la fenêtre principale
    root.config(bg="#1E1E2D")

    app = None  # Remplacez ceci par votre app réelle si nécessaire
    stats_page = StatsPage(root, app)

    stats_page.show()  # Afficher la page des statistiques
    stats_page.scan()  # Effectuer un scan et mettre à jour les stats
    stats_page.scan()  # Effectuer un autre scan et mettre à jour les stats

    root.mainloop()
