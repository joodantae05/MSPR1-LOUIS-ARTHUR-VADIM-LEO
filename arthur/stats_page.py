import tkinter as tk

class StatsPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.config(bg="#141526")  # Changer la couleur de fond de la fenêtre en gris
        self.frame = tk.Frame(root, bg="#141526")  # Changer la couleur de fond du cadre en gris

    def show(self):
        """Afficher la page"""
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        """Masquer la page"""
        self.frame.pack_forget()
