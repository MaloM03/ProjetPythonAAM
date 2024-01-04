import tkinter as tk

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

class Application : 
    
    def __init__(self, prod_page, user_name):
        self.production = prod_page
        self.production.title("Application Production")
       
        # Définir la taille initiale de la fenêtre
        self.production.geometry("400x300+750+300")

        # Création des widgets pour l'interface utilisateur
        self.create_widgets()

    def create_widgets(self):

        #===== PRODUITS =====
        # Création d'une étiquette
        user_label = tk.Label(self.production, text= "Produit")
        user_label.grid(row=0, column=0, sticky="e")
        user_label = tk.Label(self.production, text= "Produit")
        user_label.grid(row=1, column=0, sticky="e")

        # Création d'une zone de saisie
        self.user_entry = tk.Entry(self.production)
        self.user_entry.grid(row=2, column=1)
        

        

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
