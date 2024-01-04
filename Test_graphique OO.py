import tkinter as tk
global user_name
global password


class Connection:
    def __init__(self, connection_page):
        self.ID = connection_page
        self.ID.title("Connection")

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

            # Création de l'application de connexion
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

        # Création des widgets pour l'interface utilisateur
        self.create_widgets()

    def create_widgets(self):

        #===== PRODUITS =====
        # Création d'une étiquette
        user_label = tk.Label(self.production, text= "Produit")
        user_label.pack()

        # Création d'une zone de saisie
        self.user_entry = tk.Entry(self.production)
        self.user_entry.pack()

        

if __name__ == "__main__":
    # Création de la fenêtre principale
    connection_page = tk.Tk()

    prod_page = tk.Tk()
    prod_page.withdraw()
    
    # Création de l'application de connexion
    connection_app = Connection(connection_page) 

    prod_app= Application(prod_page,connection_page)

    # Lancement de la boucle principale
    connection_page.mainloop()