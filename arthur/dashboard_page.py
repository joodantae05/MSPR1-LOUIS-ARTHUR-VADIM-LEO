import tkinter as tk

class DashboardPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.config(bg="#141526")
        self.frame = tk.Frame(root, bg="#141526")
        self.result_label = tk.Label(self.frame, text="Résultats du scan", fg="white", bg="#141526", font=("Arial", 16))
        self.result_label.pack(pady=20)

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

    def show_results(self, machine_info):
        # Cette méthode affiche les résultats du scan dans le tableau de bord
        for ip, open_ports, service_info, vulnerabilities in machine_info:
            result_text = f"IP: {ip}\n"
            result_text += f"  Ports ouverts: {', '.join(map(str, open_ports)) if open_ports else 'Aucun port ouvert'}\n"
            for port in open_ports:
                service = service_info.get(port, {}).get('service', 'Inconnu')
                version = service_info.get(port, {}).get('version', 'Inconnue')
                result_text += f"    Port {port}: {service} {version}\n"
                result_text += f"    Vulnérabilités: {vulnerabilities.get(port, 'Aucune vulnérabilité détectée')}\n"
            
            result_label = tk.Label(self.frame, text=result_text, fg="white", bg="#141526", font=("Arial", 12))
            result_label.pack(pady=10)
