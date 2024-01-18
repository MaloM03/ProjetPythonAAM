import xmlrpc.client
import tkinter as tk
from tkinter import ttk

#=====PAGE D'APPLICATION=====
class Application : 
    
     #=====CREATION DE LA PAGE APPLICATION===== 
    def __init__(self, log_page, user_name):
        self.logistique = log_page
        self.logistique.title("Application Logistique")
       
        # Définir la taille initiale de la fenêtre
        self.logistique.geometry("1000x300+500+300")

        self.AjoutProd = tk.Entry(self.logistique)
        

        # Création des widgets pour l'interface utilisateur
        self.create_widgets()
        

     #===== TABLEAU PRODUITS =====
    def create_widgets(self):
        # Création du Treeview (tableau)
        self.tree = ttk.Treeview(self.logistique, columns=("Nom", "Quantité de stok", "Prix àl'unité", "Image de ref", "Code article"))

        # Configuration des colonnes
        
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Quantité de stok", text="Quantité de stok")
        self.tree.heading("Prix àl'unité", text="Prix àl'unité")
        self.tree.heading("Image de ref", text="Image de ref")
        self.tree.heading("Code article", text="Code article")


        # Ajout des données au tableau
        self.add_data_to_table()
        #self.transform_data()
        
        

        # Affichage du tableau
        self.tree.grid(row=0, column=0, sticky="nsew")
        

        # Configuration du redimensionnement de la fenêtre
        self.logistique.grid_rowconfigure(0, weight=1)
        self.logistique.grid_columnconfigure(0, weight=1)

        # Suppression de la colonne d'ID
        self.tree.column("#0", width=0, stretch=tk.NO)

     #===== SAISIE DE L'AJOUT DE PRODUCTION=====
        # Ajout du label sous le tableau
        prod_label = tk.Label(self.logistique, text="Modifié stok")
        prod_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        # Ajout du label erreur saisie 
        global prod_labelerror
        prod_labelerror = tk.Label(self.logistique, text="Saisie invalide")
        prod_labelerror.config(fg="red")
        prod_labelerror.grid(row=4, column=0, sticky="n", padx=5, pady=5)
        prod_labelerror.grid_forget() 

        # Ajout de la zone de saisie sous le label
        self.AjoutProd = tk.Entry(self.logistique)
        self.AjoutProd.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)


        # Ajout du bouton de validation
        validate_button = tk.Button(self.logistique, text="Valider", command=self.validate_entry)
        validate_button.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

        # Ajout du bouton refresh
        refresh_BP = tk.Button(self.logistique, text="refresh", command=self.refresh)
        refresh_BP.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        
     #=====AFFICHAGE DU TABLEAU DES PRODUITS===== 
    def add_data_to_table(self):
        data = []
        mo_list = [] # rajouter chelou
        for mo_dico in mo_list:
            Article = mo_dico['product_id']
            OF = mo_dico['name']
            QAP = mo_dico['product_qty']
            QDP = self.AjoutProd.get()
            DATE = mo_dico['date_planned_start']
            ligne = (Article, OF,(QDP,"/",QAP), DATE)
            data.append(ligne)

         # Efface toutes les lignes actuelles du tableau
        for item in self.tree.get_children():
           self.tree.delete(item)
         #Apres avoir effacé on re - affiche le tableau modifié 
        for item1 in data:
            self.tree.insert("", "end", values=item1)


     #=====BOUTON DE VALIDATION SAISIE STOK=====
            
            
    def validate_entry(self): 
         
         ModifStok = self.AjoutProd.get()
    
         if ModifStok.isdigit():
         # Fonction appelée lors de la validation du bouton
            self.add_data_to_table()

         # Efface la saisie AjoutProd après la validation
            self.AjoutProd.delete(0, 'end')

         #Efface l'erreur de saisie 
            prod_labelerror.grid_forget()

         else: 
            prod_labelerror.grid(row=4, column=0)

         # Efface la saisie AjoutProd après la validation
            self.AjoutProd.delete(0, 'end')
    
    def refresh(self):

          # Fonction appelée lors de la validation du bouton
            self.add_data_to_table()
            
            # Efface la saisie AjoutProd après la validation
            self.AjoutProd.delete(0, 'end')

         #Efface l'erreur de saisie 
            prod_labelerror.grid_forget()

#if __name__ == "__main__":
    # Création de la fenêtre de connection
    #global prod_page
    #global connection_page
    #connection_page = tk.Tk()
    
    # Création de la fenêtre principale + mettre invisible
    #prod_page = tk.Tk()
    #prod_page.withdraw()
    #prod_app = Application(prod_page,connection_page)
    #connection_app = Connection(connection_page,prod_page, prod_app) 
    
    
    # Loop des fenetres
    #connection_page.mainloop()
    #prod_page.mainloop()
