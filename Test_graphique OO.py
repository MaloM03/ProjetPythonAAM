import tkinter as tk
from tkinter import ttk
'''
class Connection:
    def __init__(self, connection_page):
        self.ID = connection_page
        self.ID.title("Connection")
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

        # Vérification des identifiants
        code = (user_name.lower() == "a" and password.lower() == "s") or \
               (user_name.lower() == "a" and password.lower() == "c") or \
               (user_name.lower() == "m" and password.lower() == "m")

        if code:
            # Fermeture auto de la fenêtre de connexion
            self.ID.destroy()

            # Affichage de l'application 
            prod_page.deiconify()
            

            
        else:
            # Création d'une fenêtre d'erreur
            error_window = tk.Toplevel(self.ID)
            error_window.title("Error")

            # Ajout des éléments à la fenêtre d'erreur
            error_label = tk.Label(error_window, text="User/Password incorrect")
            error_label.pack()

            # Effacement des champs de saisie
            self.user_entry.delete(0, "end")
            self.password_entry.delete(0, "end")
'''
class Application : 
    
    def __init__(self, prod_page, user_name):
        self.production = prod_page
        self.production.title("Application Production")
       
        # Définir la taille initiale de la fenêtre
        self.production.geometry("800x300+750+300")

        # Création des widgets pour l'interface utilisateur
        self.create_widgets()

    def create_widgets(self):

        #===== TABLEAU PRODUITS =====
        # Création du Treeview (tableau)
        self.tree = ttk.Treeview(self.production, columns=("Nom", "N° OF", "Quantité à produire", "Echéance"))

        # Configuration des colonnes
        
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("N° OF", text="N° OF")
        self.tree.heading("Quantité à produire", text="Quantité à produire")
        self.tree.heading("Echéance", text="Echéance")

        # Ajout des données au tableau
        self.add_data_to_table()

        # Affichage du tableau
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Configuration du redimensionnement de la fenêtre
        self.production.grid_rowconfigure(0, weight=1)
        self.production.grid_columnconfigure(0, weight=1)

        # Suppression de la colonne d'ID
        self.tree.column("#0", width=0, stretch=tk.NO)

        #===== SAISIE DE L'AJOUT DE PRODUCTION
        prod_label = tk.Label(self.production, text="Ajouter une production : ")
        prod_label.grid(row=5, column=0)

        # Création d'une zone de saisie
        self.prod_entry = tk.Entry(self.production)
        self.prod_entry.grid(row=5, column=1)

    def add_data_to_table(self):
        # Ajoutez vos données au tableau
        data = [
            ("Peluche 1", "0555", "2000/5000", "05/01/2024", "Valeur1-4"),
            #("2", "Valeur2-1", "Valeur2-2", "Valeur2-3", "Valeur2-4"),
            #("3", "Valeur3-1", "Valeur3-2", "Valeur3-3", "Valeur3-4"),
            # ... Ajoutez autant de lignes que nécessaire
        ]
        for item in data:
            self.tree.insert("", "end", values=item)

        
   
        

        

if __name__ == "__main__":
    # Création de la fenêtre principale
    prod_page = tk.Tk()
    #prod_page.withdraw()

    # Création de la fenetre de loging
    connection_page = tk.Tk()

    # Création de l'application de connexion
   # connection_app = Connection(connection_page) 
    prod_app= Application(prod_page,connection_page)

    # Lancement de l'application
    connection_page.mainloop()
