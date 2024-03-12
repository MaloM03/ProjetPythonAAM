import tkinter as tk
from tkinter import ttk
import xmlrpc.client
import re
from operator import itemgetter

#=====PAGE D'APPLICATION=====
class Application : 
    
     #=====CREATION DE LA PAGE APPLICATION===== 
    def __init__(self, prod_page, user_name):
        self.selected_id = None
        self.production = prod_page
        self.production.title("AMA - Application Production")
       
        # Définir la taille initiale de la fenêtre
        self.production.geometry("1200x600+750+300")

        self.AjoutProd = tk.Entry(self.production)
        

        # Création des widgets pour l'interface utilisateur
        self.create_widgets()
        
    def set_odoo(self, currentOdoo):
        self.odooRef = currentOdoo
        
     #===== TABLEAU PRODUITS =====
    def create_widgets(self):
        # Création du Treeview (tableau)
        self.tree = ttk.Treeview(self.production, columns=("Nom", "N° OF", "Quantité à produire", "Echéance", "CreateDate"))

        # Configuration des colonnes
        
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("N° OF", text="N° OF")
        self.tree.heading("Quantité à produire", text="Nombre d'article réalisé")
        self.tree.heading("Echéance", text="Date de livraison")
        self.tree.heading("CreateDate", text="Date de création")
      
        self.tree.bind('<<TreeviewSelect>>', self.on_select) #lier la fonction on_select a la selection de ligne dans le tableau
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
        prod_label = tk.Label(self.production, text="Modifier le nombre de pièce réaliser sur l'OF sélectioné :")
        prod_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        # Ajout de la zone de saisie sous le label
        self.AjoutProd = tk.Entry(self.production)
        self.AjoutProd.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Ajout du bouton de validation
        validate_button = tk.Button(self.production, text="Valider", command=self.validate_entry)
        validate_button.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

        # Ajout du bouton refresh
        refresh_BP = tk.Button(self.production, text="refresh", command=self.refresh)
        refresh_BP.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        
     #=====AFFICHAGE DU TABLEAU DES PRODUITS===== 
    def add_data_to_table(self, OdooData):
        data = []
        for mo_dico in OdooData :
            
            Article = mo_dico['product_id'][1]
            OF = mo_dico['name']
            QAP = mo_dico['product_qty']
            QDP = mo_dico['qty_producing']
            DATE = mo_dico['date_planned_start']
            CREATION = mo_dico['create_date']
            ligne = (Article, OF,(QDP, "/" ,QAP), DATE, CREATION)
            data.append(ligne)

        #trier des data en fonction de la date prévu de prod
        data.sort(key=itemgetter(3))

         # Efface toutes les lignes actuelles du tableau
        for item in self.tree.get_children():
           self.tree.delete(item)
         #Apres avoir effacé on re - affiche le tableau modifié 
        for item1 in data:
            self.tree.insert("", "end", values=item1)

     #=====BOUTON DE VALIDATION SAISIE PROD=====
    def validate_entry(self): 
        # Fonction appelée lors de la validation du bouton
        valeur = self.AjoutProd.get()
        if valeur.isdigit(): # La valeur est un entier
            if self.selected_id is not None:
                self.odooRef.update_manufacturing_order_qty_producing(self.selected_id, valeur)
                print("Modified ID :")
                print(self.selected_id)
                print("Valeur emise : ")
                print(valeur)
                self.selected_id = None
                self.refresh()
                self.effacer_ajout_prod()
        else: # La valeur n'est pas un entier
            print("la valeur n'est pas un entier")
            self.effacer_ajout_prod()
        
        

        #self.AjoutProd.set("")
        #self.AjoutProd.delete(0, "end")
        #self.AjoutProd.update()

         
    def on_select(self, event):
        # Récupère l'élément sélectionné dans le tableau
        selected_item = self.tree.selection()

        # Vérifie si un élément est effectivement sélectionné
        if selected_item:
            # Récupère les valeurs des colonnes de l'élément sélectionné
            values = self.tree.item(selected_item)['values']
            print("Éléments sélectionnés:", values)

            # Extrait le nombre de la chaîne "WH/MO/00006"
            self.selected_id = self.extract_number(values[1])
            print("Numéro extrait:", self.selected_id)

    def extract_number(self, input_string):
        # Utilise une expression régulière pour extraire les chiffres de la chaîne
        match = re.search(r'\d+', input_string)
        if match:
            return int(match.group())
        else:
            return None
        
    def refresh(self):
        #Actualiser le tableau après une modification

        self.odooRef.getFields()
        data = self.odooRef.getManufOrderToDo()
        self.add_data_to_table(data)
        self.effacer_ajout_prod()

    def effacer_ajout_prod(self):
        """Fonction pour effacer le contenu de la zone de saisie 'AjoutProd'."""
        self.AjoutProd.delete(0, tk.END)