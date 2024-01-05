import tkinter as tk
from tkinter import ttk
import xmlrpc.client

#=====PROGRAMME DE CONNECTION A ODOO=====
class IF_ErpOdoo:
    "Classe objet d'interface de l'ERP Odoo en XML-RPC"
    def __init__(self, erp_ipaddr, erp_port, erp_db, erp_user, erp_pwd):
        "Methode Constructeur de Classe"
        print("##IF_ErpOdoo Constructor##")
        self.mErpIpAddr = erp_ipaddr
        self.mErpIpPort = erp_port
        self.mUserId = 0
        self.mErpDB = erp_db
        self.mErpUser = erp_user
        self.mErpPwd = erp_pwd
        self.mModels = None
        self.mOdooVersion = 'Inconnue'
        self.mListFields = []
        #self.mErpUser = input("Entrez votre identifiant Odoo : ")
        #self.mErpPwd = input("Entrez votre mot de passe Odoo : ")
    
    def init(self):
        self.mModels = None
        self.mOdooVersion = 'Inconnue'
        self.mListFields = []

    def __del__(self):
        
        "Methode Constructeur de Classe"
        print("##IF_ErpOdoo Destructor##")

    def connect(self):
        """Methode de connexion à l'ERP Odoo"""
        erp_url = f'http://{self.mErpIpAddr}:{self.mErpIpPort}'
        print("Connexion ODOO")
        print(f"@URL={erp_url}")
        self.init()
        try:
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(erp_url))
            version = common.version()
            self.mOdooVersion = version['server_serie']
            print(f"Odoo version={self.mOdooVersion}")
        except ConnectionRefusedError:
            print("Odoo Server not found or connection rejected")
        else:
            self.mUser_id = common.authenticate(self.mErpDB, self.mErpUser, self.mErpPwd, {})
            print(f"Odoo authentification:{self.mUser_id}")
        if(self.mUser_id!=False):
            self.mModels = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(erp_url))
            access = self.mModels.execute_kw(self.mErpDB, self.mUser_id, self.mErpPwd,
                'mrp.production', 'check_access_rights',
                ['write'], {'raise_exception': False})
            print(f"Manufactoring Order write access rights : {access}")
        else:
            print(f'Odoo Server authentification rejected : DB={self.mErpDB} User={self.mErpUser}')
    
    def setServer(self, erp_ipaddr, erp_port):
        self.mErpIpAddr = erp_ipaddr
        self.mErpIpPort = erp_port
        self.connect()

    def getFields(self, base='mrp.production'):
        if(self.mModels!=None):
            listing = self.mModels.execute_kw(self.mErpDB, self.mUser_id, self.mErpPwd,
                base, 'fields_get',
                [], {'attributes': []})
            self.mListFields.clear()
        for attr in listing:
            self.mListFields.append(attr)
            nb_attr = len(self.mListFields)
            print(f'*** {base} [{nb_attr}]***')
    
    def printFields(self):
        for attr in self.mListFields:
            print(f' - {attr}')

    def getManufOrderToDo(self):
        if(self.mModels!=None):
            fields =['name', 'date_planned_start', 'product_id', 'product_qty', 'qty_producing', 'state']
            limit = 10
            global mo_list
            mo_list = self.mModels.execute_kw(self.mErpDB, self.mUser_id, self.mErpPwd,
                'mrp.production', 'search_read',
                [[('state', '=', 'confirmed'), ('qty_produced', '!=', 'product_qty')]],
                {'fields': fields, 'limit': limit})
            for mo_dico in mo_list:
                print(f'----------------------------')
                for k in mo_dico.keys():
                    print(f' - {k} : {mo_dico[k]}')

    def getArticle(self):
        if self.mModels is not None:
            fields = ['display_name','qty_available']
            limit = 100
            global mo_list
            mo_list = self.mModels.execute_kw(self.mErpDB,self.mUser_id,self.mErpPwd,
                'product.product','search_read',
                [],
                {'fields': fields, 'limit': limit})
            for mo_dico in mo_list:
                print(f'----------------------------')
                for k in mo_dico.keys():
                    print(f' - {k} : {mo_dico[k]}')

#=====PAGE DE CONNECTION=====
class Connection:
    def __init__(self, connection_page):
        self.ID = connection_page
        self.ID.title("Connection")
        self.ID.geometry("200x200+850+300")

        # Création des widgets pour l'interface utilisateur
        self.create_widgets()

    def create_widgets(self):
        #===== USER =====
        user_label = tk.Label(self.ID, text="User : ")
        user_label.pack()

        # Création d'une zone de saisie 
        self.user_var = tk.StringVar()
        self.user_entry = ttk.Entry(self.ID, textvariable=self.user_var)
        self.user_entry.pack()

        #===== PASSWORD =====
        # Création d'une étiquette
        password_label = tk.Label(self.ID, text="Password : ")
        password_label.pack()

        # Création d'une zone de saisie
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.ID, textvariable=self.password_var, show='*')
        self.password_entry.pack()

        # Lier l'événement de pression de la touche Entrée à la fonction Validation
        self.password_entry.bind("<Return>", self.validation)

    def validation(self, event):
        user_name = self.user_var.get()
        password = self.password_var.get()

        # Vérification des identifiants Odoo
        # Replace la vérification des identifiants
        odoo_credentials_valid = True

        if odoo_credentials_valid:
            # Fermeture auto de la fenêtre de connexion
            self.ID.destroy()

            # Affichage de l'application
            print("affichage page PROD")

            # Utiliser les identifiants Odoo (user_name, password) ici
            print("User:", user_name)
            print("Password:", password)
        else:
            # Création d'une fenêtre d'erreur
            error_window = tk.Toplevel(self.ID)
            error_window.title("Error")
            error_window.geometry("200x60+850+350")

            # Ajout des éléments à la fenêtre d'erreur
            error_label = tk.Label(error_window, text="User/Password incorrect")
            error_label.pack()

            # Effacement des champs de saisie
            self.user_var.set("")
            self.password_var.set("")

if __name__ == "__main__":
    connection_page = tk.Tk()
    connection_app = Connection(connection_page)
    connection_page.mainloop()

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
    def add_data_to_table(self):
        data = []
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

     #=====BOUTON DE VALIDATION SAISIE PROD=====
    def validate_entry(self): 
         # Fonction appelée lors de la validation du bouton
         self.add_data_to_table()

         # Efface la saisie AjoutProd après la validation
         self.AjoutProd.delete(0, 'end')
    
class MaFenetre(tk.Tk):
    def __init__(self):
        super().__init__()
       
        self.title("Application Production")
       
        # Définir la taille initiale de la fenêtre
        self.geometry("800x300+750+300")
        

        # Création du Treeview (tableau)
        self.entry_test_chiffre = tk.Entry(self)
        self.create_widgets()
        
        # Ajout du label sous le tableau
        self.label = tk.Label(self, text="Ajouter une production")
        self.label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        # Ajout de la zone de saisie sous le label
        self.entry_test_chiffre = tk.Entry(self)
        self.entry_test_chiffre.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Ajout du bouton de validation
        self.button_valider_test_chiffre = tk.Button(self, text="Valider", command=self.validate_entry)
        self.button_valider_test_chiffre.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

        # Ajout du label d'erreur syntaxe
        self.label_invalide = tk.Label(self, text="Invalide", fg="red")
        self.label_invalide.grid(row=4, column=0, sticky="w", padx=5, pady=5)
    
    #===== TABLEAU PRODUITS =====
    def create_widgets(self):
        # Création du Treeview (tableau)
        self.tree = ttk.Treeview(self, columns=("Nom", "N° OF", "Quantité à produire", "Echéance"))

        # Configuration des colonnes
        
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("N° OF", text="N° OF")
        self.tree.heading("Quantité à produire", text="Quantité à produire")
        self.tree.heading("Echéance", text="Echéance")
        
        # Lier l'événement de sélection à la fonction
        self.tree.bind("<ButtonRelease-1>", self.selection_ligne_tableau)

        # Ajout des données au tableau
        self.add_data_to_table()
        #self.transform_data()
        
        # Affichage du tableau
        self.tree.grid(row=0, column=0, sticky="nsew")
    
        # Configuration du redimensionnement de la fenêtre
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Suppression de la colonne d'ID
        self.tree.column("#0", width=0, stretch=tk.NO)
    
    
    
    #=====AFFICHAGE DU TABLEAU DES PRODUITS===== 
    def add_data_to_table(self):
        data = []
        for mo_dico in mo_list:
            Article = mo_dico['product_id']
            OF = mo_dico['name']
            QAP = mo_dico['product_qty']
            QDP = self.entry_test_chiffre.get()
            DATE = mo_dico['date_planned_start']
            ligne = (Article, OF,(QDP,"/",QAP), DATE)
            data.append(ligne)

         # Efface toutes les lignes actuelles du tableau
        for item in self.tree.get_children():
           self.tree.delete(item)
         #Apres avoir effacé on re - affiche le tableau modifié 
        for item1 in data:
            self.tree.insert("", "end", values=item1)

    def selection_ligne_tableau(self, event):
        # Récupérer la ligne sélectionnée
        selected_item = self.tree.selection()
        if selected_item:
            # Afficher le label "test chiffre" et la zone de saisie
            self.label.pack(pady=5)
            self.entry_test_chiffre.pack(pady=5)
            self.button_valider_test_chiffre.pack(pady=5)
            # Masquer le label "invalide"
            self.label_invalide.pack_forget()
    
    #=====BOUTON DE VALIDATION SAISIE PROD=====
    def validate_entry(self): 
         # Fonction appelée lors de la validation du bouton
         self.add_data_to_table()

         # Efface la saisie AjoutProd après la validation
         self.AjoutProd.delete(0, 'end')

    def valider_saisie_test_chiffre(self):
        # Récupérer la valeur de la zone de saisie
        valeur_saisie = self.entry_test_chiffre.get()

        # Vérifier si la valeur saisie est un nombre
        try:
            float(valeur_saisie)
        except ValueError:
            # Afficher le label "invalide" si ce n'est pas un nombre
            self.label_invalide.pack(pady=5)
            return

        # Récupérer la ligne sélectionnée
        selected_item = self.tree.selection()
        if selected_item:
            # Mettre à jour la valeur dans la colonne "Chiffre" de la ligne sélectionnée
            self.tree.item(selected_item, values=(self.tree.item(selected_item, "values")[0], valeur_saisie))
            # Cacher le label "invalide" si la mise à jour réussit
            self.label_invalide.pack_forget()
            # Efface la saisie AjoutProd après la validation
            self.entry_test_chiffre.delete(0, 'end')



#=====MAIN=====
if __name__ == "__main__":

    ifOdoo = IF_ErpOdoo("172.31.10.171", "8069","amaDB", "vente", "ventepython2024")
    ifOdoo.connect()
    print(f'=> Version : {ifOdoo.mOdooVersion}')
    ifOdoo.setServer("172.31.10.171", "8069")
    ifOdoo.connect()
    print(f'=> Version : {ifOdoo.mOdooVersion}')

    ifOdoo.getFields()
    ifOdoo.getManufOrderToDo()
    #print(mo_list)
    #print(Application.transform_data(mo_list))

    # Création de la fenêtre principale
    prod_page = tk.Tk()
    prod_page.withdraw()

    # Création de la fenetre de loging
    connection_page = tk.Tk()

    # Création de l'application de connexion
    connection_app = Connection(connection_page) 
    prod_app= Application(prod_page,connection_page)

    # Lancement de l'application
    app = MaFenetre()
    app.mainloop()
    connection_page.mainloop()



