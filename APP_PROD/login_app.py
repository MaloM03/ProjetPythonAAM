import tkinter as tk
from tkinter import ttk
import xmlrpc.client
from odoo import *

class Connection:
    def __init__(self, connection_page, prod_page, prod_app):
        self.prod_app = prod_app
        self.prod_page = prod_page
        self.ID = connection_page
        self.ID.title("Connection App Prod")
        self.ID.geometry("200x150+850+300")


        # Création des widgets pour l'interface utilisateur
        self.create_widgets()

    def create_widgets(self):
        #===== USER =====
        # Création d'une étiquette
        user_label = tk.Label(self.ID, text="User : ")
        user_label.pack()

        # Création d'une zone de saisie
        self.user_entry = tk.Entry(self.ID)
        self.user_entry.pack()

        #===== PASSWORD =====
        # Création d'une étiquette
        password_label = tk.Label(self.ID, text="Password : ")
        password_label.pack()

        # Création d'une zone de saisie
        self.password_entry = tk.Entry(self.ID, show='*')
        self.password_entry.pack()

        # Lier l'événement de pression de la touche Entrée à la fonction Validation
        self.password_entry.bind("<Return>", self.validation)

    def validation(self, event):
        user_name = self.user_entry.get()
        password = self.password_entry.get()
       
        ifOdoo = IF_ErpOdoo("172.31.10.188", "8069","amaDB", user_name, password)
        if ifOdoo.connect():
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
            error_window.title("Error")
            error_window.geometry("200x60+850+350")

            # Ajout des éléments à la fenêtre d'erreur
            error_label = tk.Label(error_window, text="User/Password incorrect")
            error_label.pack()

            # Effacement des champs de saisie
            self.user_entry.delete(0, "end")
            self.password_entry.delete(0, "end")
