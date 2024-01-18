import tkinter as tk
from tkinter import ttk
import xmlrpc.client

#=====PAGE D'APPLICATION=====
class Application : 
    
     #=====CREATION DE LA PAGE APPLICATION===== 
    def __init__(self, prod_page, user_name):
        self.production = prod_page
        self.production.title("Application Production")
       
        # Définir la taille initiale de la fenêtre
        self.production.geometry("800x300+750+300")

        self.AjoutProd = tk.Entry(self.production)
        

        # Création des widgets pour l'interface utilisateur
        self.create_widgets()
        

     #===== TABLEAU PRODUITS =====
    def create_widgets(self):
        # Création du Treeview (tableau)
        self.tree = ttk.Treeview(self.production, columns=("Nom", "N° OF", "Quantité à produire", "Echéance"))

        # Configuration des colonnes
        
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("N° OF", text="N° OF")
        self.tree.heading("Quantité à produire", text="Quantité à produire")
        self.tree.heading("Echéance", text="Echéance")

        # Ajout des données au tableau
        #self.add_data_to_table()
        #self.transform_data()
        
        

        # Affichage du tableau
        self.tree.grid(row=0, column=0, sticky="nsew")
        

        # Configuration du redimensionnement de la fenêtre
        self.production.grid_rowconfigure(0, weight=1)
        self.production.grid_columnconfigure(0, weight=1)

        # Suppression de la colonne d'ID
        self.tree.column("#0", width=0, stretch=tk.NO)

     #===== SAISIE DE L'AJOUT DE PRODUCTION=====
        # Ajout du label sous le tableau
        prod_label = tk.Label(self.production, text="Ajouter une production")
        prod_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        # Ajout de la zone de saisie sous le label
        self.AjoutProd = tk.Entry(self.production)
        self.AjoutProd.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Ajout du bouton de validation
        validate_button = tk.Button(self.production, text="Valider", command=self.validate_entry)
        validate_button.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        
     #=====AFFICHAGE DU TABLEAU DES PRODUITS===== 
    def add_data_to_table(self, OdooData):
        data = []
        for mo_dico in OdooData :
            
            Article = mo_dico['product_id']
            OF = mo_dico['name']
            QAP = mo_dico['product_qty']
            QDP = mo_dico['qty_producing']
            DATE = mo_dico['date_planned_start']
            ligne = (Article, OF,(QDP, "/" ,QAP), DATE)
            data.append(ligne)

         # Efface toutes les lignes actuelles du tableau
        for item in self.tree.get_children():
           self.tree.delete(item)
         #Apres avoir effacé on re - affiche le tableau modifié 
        for item1 in data:
            self.tree.insert("", "end", values=item1)

     #=====BOUTON DE VALIDATION SAISIE PROD=====
    def validate_entry(self): 
         # Fonction appelée lors de la validation du bouton
         self.add_data_to_table()

         # Efface la saisie AjoutProd après la validation
         self.AjoutProd.delete(0, 'end')
         