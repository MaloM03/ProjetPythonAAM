import tkinter as tk
from tkinter import ttk
import xmlrpc.client

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
    def __del__(self):
        
        "Methode Constructeur de Classe"
        print("##IF_ErpOdoo Destructor##")

    def connect(self):
        "Methode de connexion à l'ERP Odoo"
        erp_url = f'http://{self.mErpIpAddr}:{self.mErpIpPort}'
        print("Connexion ODOO")
        print(f"@URL={erp_url}")
        try:
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(erp_url))
            version = common.version()
            print(f"Odoo version={version['server_serie']}")
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

    def getFields(self):
        if(self.mModels!=None):
            listing = self.mModels.execute_kw(self.mErpDB, self.mUser_id, self.mErpPwd,
                'mrp.production', 'fields_get',
                [], {'attributes': []})
        for attr in listing:
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
            fields = ['product_id', 'qty_producing']
            limit = 100
            global mo_list
            mo_list = self.mModels.execute_kw(self.mErpDB,self.mUser_id,self.mErpPwd,
                'mrp.production','search_read',
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

        for item1 in data:
            self.tree.insert("", "end", values=item1)
   
    def validate_entry(self): 
         # Fonction appelée lors de la validation du bouton
         self.add_data_to_table()

         # Efface la saisie AjoutProd après la validation
         self.AjoutProd.delete(0, 'end')
    

if __name__ == "__main__":

    ifOdoo = IF_ErpOdoo("172.31.10.171", "8069","amaDB", "vente", "ventepython2024")
    ifOdoo.connect()
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
    connection_page.mainloop()



