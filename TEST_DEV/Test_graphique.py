import tkinter as tk

def Validation(event):
    UserName = user_entry.get()
    Password = password_entry.get()
    
    Code = (UserName.lower() == "a"  and Password.lower() == "s") or \
       (UserName.lower() == "a"  and Password.lower() == "c") or \
       (UserName.lower() == "m"  and Password.lower() == "m")
    

    if Code : 
         # Création d'une nouvelle fenêtre
         App = tk.Tk()
         App.title("ERP.Production")

         # Ajoutez des éléments à la nouvelle fenêtre
         new_label = tk.Label(App, text="Bienvenue sur la deuxième page !")
         new_label.pack()

         #fermeture auto de la fenetre de connection et Error
         Connection.destroy()

    else : 
         #Création d'une fenêtre d'erreur
         fenetredemerde = tk.Toplevel(Connection)
         fenetredemerde.title("Error")

         # Ajoutez des éléments à lafenêtre d'erreur
         new_label = tk.Label(fenetredemerde, text="User/ Password incorect")
         new_label.pack()
         user_entry.delete(0,"end")
         password_entry.delete(0,"end")
                   
# Création de la fenêtre principale
Connection = tk.Tk()
Connection.title("Connection")

#===== USER =====
# Création d'une étiquette
user_label = tk.Label(Connection, text="User : ")
user_label.pack()

# Création d'une zone de saisie
user_entry = tk.Entry(Connection)
user_entry.pack()

#===== PASSWORD =====
# Création d'une étiquette
password_label = tk.Label(Connection, text="Password : ")
password_label.pack()

# Création d'une zone de saisie
password_entry = tk.Entry(Connection)
password_entry.pack()

# Lier l'événement de pression de la touche Entrée à la fonction
password_entry.bind("<Return>", Validation)

# Lancement de la boucle principale
Connection.mainloop()

