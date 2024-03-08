from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

import xmlrpc.client
from odoo import *

class Connection:
    def __init__(self, connection_page, prod_page, prod_app):
        self.prod_app = prod_app
        self.prod_page = prod_page
        self.ID = connection_page
        self.ID.title("AMA - Application Production")
        self.ID.geometry("400x300+850+300")

        # Création des widgets pour l'interface utilisateur
        self.create_widgets()

    def create_widgets(self):

        # LOGO
        logo = Image.open("APP_PROD/ressources/logo.png")
        logo = logo.resize((100, 100))
        logo_tk = ImageTk.PhotoImage(logo) # Conversion de l'image en format Tkinter
        logo_label = tk.Label(self.ID, image=logo_tk) # Création d'un label pour afficher l'image
        #logo_label = logo_label.config(width=100, height=50)
        logo_label.lift()
        logo_label.pack()

        #Main label Titre
        main_label = tk.Label(self.ID, text="Application Production", font=("Arial", 16),padx=0, pady=25)
        main_label.pack()

        #===== USER =====
        # Création d'une étiquette
        user_label = tk.Label(self.ID, text="Utilisateur : ",padx=0, pady=5)
        user_label.pack()

        # Création d'une zone de saisie
        self.user_entry = tk.Entry(self.ID)
        self.user_entry.pack()

        #===== PASSWORD =====
        # Création d'une étiquette
        password_label = tk.Label(self.ID, text="Mot de passe : ",padx=0, pady=5)
        password_label.pack()

        # Création d'une zone de saisie
        self.password_entry = tk.Entry(self.ID, show='*')
        self.password_entry.pack()

        # Lier l'événement de pression de la touche Entrée à la fonction Validation
        self.password_entry.bind("<Return>", self.validation)

        bp_validation = tk.Button(self.ID,text="Connection",font=("Arial", 16),padx=0,pady=0,command=self.connection)
        bp_validation.pack()

    def validation(self, event):
        self.connection()

    def connection(self):
        user_name = self.user_entry.get()
        password = self.password_entry.get()
       
        ifOdoo = IF_ErpOdoo("localhost", "8069","amaDB", user_name, password)
        if ifOdoo.connect():
            self.prod_app.set_odoo(ifOdoo)
            # Fermeture auto de la fenêtre de connexion
            self.ID.destroy()

            # Affichage de l'application 
            print("affichage page PROD")
            self.prod_page.deiconify()
            ifOdoo.getFields()
            data = []
            data = ifOdoo.getManufOrderToDo()
            self.prod_app.add_data_to_table(data)
            
        else:
            # Création d'une fenêtre d'erreur
            error_window = tk.Toplevel(self.ID)
            error_window.title("Erreur de connection")
            error_window.geometry("400x120+850+350")

            # Ajout des éléments à la fenêtre d'erreur
            error_label = tk.Label(error_window, text="Vos identifiants sont incorrect \n ou problème de connection au serveur",font=("Arial", 12),padx=0,pady=10)
            error_label.pack()

            # Effacement des champs de saisie
            self.user_entry.delete(0, "end")
            self.password_entry.delete(0, "end")
