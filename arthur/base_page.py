from tkinter import BOTH, Frame, Label, Button, TOP, LEFT, RIGHT, X, HORIZONTAL
from tkinter.ttk import Progressbar

class BasePage:
    def __init__(self, root, app, title, tabs):
        self.root = root
        self.app = app
        self.title = title
        self.tabs = tabs
        self.frame = Frame(self.root, bg='#313438')

        # Frame contenant le titre du site à gauche
        self.header_frame = Frame(self.frame, bg='#202225', width=600, height=100)
        self.header_frame.pack(side=TOP, fill=X)
        
        # Titre à gauche
        self.label_titre = Label(
            self.header_frame,
            text=self.title,
            font=("Helvetica", 20, "bold"),
            fg="white",
            bg="#202225",
            wraplength=500,
            justify="left"
        )
        self.label_titre.pack(side=LEFT, padx=20, pady=20)

        # Barre de navigation avec les onglets à droite
        self.tab_frame = Frame(self.header_frame, bg='#202225')
        self.tab_frame.pack(side=RIGHT)

        # Création des onglets dynamiquement
        for tab_name, tab_command in self.tabs.items():
            tab = Button(self.tab_frame, text=tab_name, font=("Helvetica", 14), bg="#202225", fg="white", relief="flat", command=tab_command)
            tab.pack(side=LEFT, padx=10)

        self.show()

    def show(self):
        """Affiche la page"""
        self.frame.pack(fill=BOTH, expand=True)

    def hide(self):
        """Cache la page"""
        self.frame.pack_forget()
