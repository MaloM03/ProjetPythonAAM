import tkinter as tk
from tkinter import ttk

#=====PAGE DE CONNECTION=====
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
            error_window.geometry("200x60+850+350")

            # Ajout des éléments à la fenêtre d'erreur
            error_label = tk.Label(error_window, text="User/Password incorrect")
            error_label.pack()

            # Effacement des champs de saisie
            self.user_entry.delete(0, "end")
            self.password_entry.delete(0, "end")

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
        self.add_data_to_table()

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
        

    def add_data_to_table(self):
        Article = "Peluche 1"
        OF = "45785"
        QAP = 5000
        QDP = self.AjoutProd.get()
        DATE = "05/01/2024"
        # Efface toutes les lignes actuelles du tableau
        for item in self.tree.get_children():
           self.tree.delete(item)

        # Ajoutez vos données au tableau
        data = [
            (Article, OF,(QDP,"/",QAP), DATE),
            #("2", "Valeur2-1", "Valeur2-2", "Valeur2-3", "Valeur2-4"),
            #("3", "Valeur3-1", "Valeur3-2", "Valeur3-3", "Valeur3-4"),
            # ... Ajoutez autant de lignes que nécessaire
        ]
        for item in data:
            self.tree.insert("", "end", values=item)

    def validate_entry(self):
        # Fonction appelée lors de la validation du bouton
        self.add_data_to_table()

        # Efface la saisie AjoutProd après la validation
        self.AjoutProd.delete(0, 'end')

if __name__ == "__main__":
    # Création de la fenêtre principale
    prod_page = tk.Tk()
    prod_page.withdraw()

    # Création de la fenetre de loging
    connection_page = tk.Tk()

    # Création de l'application de connexion
    connection_app = Connection(connection_page) 
    prod_app= Application(prod_page,connection_page)

    # Lancement de l'application
    connection_page.mainloop()


