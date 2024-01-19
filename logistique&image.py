import xmlrpc.client
import tkinter as tk
from tkinter import ttk
import base64
from io import BytesIO
from PIL import Image
from PIL import ImageTk


def display_resized_image_in_tkinter(encoded_string, width=150, height=150):
    
    # Décode la chaîne base64
    decoded_bytes = base64.b64decode(encoded_string)

    # Crée une image à partir des données décodées
    original_image = Image.open(BytesIO(decoded_bytes))

    # Redimensionne l'image
    resized_image = original_image.resize((width, height))

    # Crée une fenêtre Tkinter
    root = tk.Tk()
    root.title("Resized Image Decoding")
    root.geometry("200x150+850+300")
    

    # Convertit l'image redimensionnée en format Tkinter
    global tk_image
    tk_image = ImageTk.PhotoImage(resized_image)

    # Crée un widget Label pour afficher l'image
    label = tk.Label(root, image=tk_image)
    label.pack()
    root.destroy()

    # Lance la boucle principale Tkinter
    root.mainloop()


#=====PROGRAMME DE CONNECTION A ODOO====
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
            return False
        else:
            self.mUser_id = common.authenticate(self.mErpDB, self.mErpUser, self.mErpPwd, {})
            print(f"Odoo authentification:{self.mUser_id}")
        if(self.mUser_id!=False):
            self.mModels = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(erp_url))
            access = self.mModels.execute_kw(self.mErpDB, self.mUser_id, self.mErpPwd,
                'mrp.production', 'check_access_rights',
                ['write'], {'raise_exception': False})
            print(f"Manufactoring Order write access rights : {access}")
            return True
        else:
            print(f'Odoo Server authentification rejected : DB={self.mErpDB} User={self.mErpUser}')
            return False
    
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
            return mo_list

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
            return mo_list
    
    def getImage(self):
        global Image1
        global Image2
        global Image3
        global Image4
        if self.mModels is not None:
            fields = ['image_1920','list_price']
            limit = 100
            global mo_list
            mo_list = self.mModels.execute_kw(self.mErpDB,self.mUser_id,self.mErpPwd,
                'product.template','search_read',
                [],
                {'fields': fields, 'limit': limit})
            for mo_dico in mo_list:
                print(f'----------------------------')
                display_resized_image_in_tkinter(mo_dico['image_1920'])
                
                for k in mo_dico.keys():
                    print(f' - {k} : {mo_dico[k]}')
                    print(mo_dico[k])
                    if mo_dico[k] ==  1 :
                        Image1 = tk_image
                        print(f'----------------------------')
                        print("ok c'est bon")
                    if mo_dico[k] ==  2 :
                        Image2 = tk_image
                        print(f'----------------------------')
                        print("ok c'est bon 2")
                    if mo_dico[k] ==  3 :
                        Image3 = tk_image
                        print(f'----------------------------')
                        print("ok c'est bon 3")
                    if mo_dico[k] ==  4 :
                        Image4 = tk_image
                        print(f'----------------------------')
                        print("ok c'est bon 4")

class Connection:
    def __init__(self, connection_page, prod_page, prod_app):
        self.prod_app = prod_app
        self.prod_page = prod_page
        self.ID = connection_page
        self.ID.title("Connection App Prod")
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
       
        ifOdoo = IF_ErpOdoo("172.31.10.188", "8069","amaDB", user_name, password)
        if ifOdoo.connect():
            # Fermeture auto de la fenêtre de connexion
            self.ID.destroy()

            # Affichage de l'application 
            print("affichage page PROD")
            self.prod_page.deiconify()
            ifOdoo.getFields()
            data = []
            data = ifOdoo.getArticle()
            self.prod_app.add_data_to_table(data)
            
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
      self.tree = ttk.Treeview(self.logistique, columns=("Nom", "Quantité de stok", "Prix àl'unité", "Code article"))

        # Configuration des colonnes
        
      self.tree.heading("Nom", text="Nom")
      self.tree.heading("Quantité de stok", text="Quantité de stok")
      self.tree.heading("Prix àl'unité", text="Prix àl'unité")
      self.tree.heading("Code article", text="Code article")


      # Ajout des données au tableau
      #self.add_data_to_table()
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

      bouton1= tk.Button(self.logistique, text="Image1", command=self.BP4)
      bouton1.grid(row=0, column=2, sticky="n", padx=5, pady=5)
      
      bouton2 = tk.Button(self.logistique, text="Image2", command=self.BP3)
      bouton2.grid(row=0, column=2, sticky="s", padx=5, pady=5)
      
      bouton3 = tk.Button(self.logistique, text="Image3", command=self.BP1)
      bouton3.grid(row=0, column=3, sticky="n", padx=5, pady=5)

      bouton4 = tk.Button(self.logistique, text="Image4", command=self.BP2)
      bouton4.grid(row=0, column=3, sticky="s", padx=5, pady=5)

     #=====AFFICHAGE DU TABLEAU DES PRODUITS===== 
   def add_data_to_table(self, OdooData):
      data = []
      for mo_dico in OdooData :
         
         Nom = mo_dico['display_name']
         Stok = mo_dico['qty_available']
         Prix = 2 #mo_dico['product_qty']
         #QDP = 2 #mo_dico['qty_producing']
         Code = "4de56" #mo_dico['date_planned_start']
         ligne = (Nom, Stok,Prix,Code)
         data.append(ligne)
         
         # Efface toutes les lignes actuelles du tableau
         for item in self.tree.get_children():
           self.tree.delete(item)
         #Apres avoir effacé on re - affiche le tableau modifié 
         for item1 in data:
            self.tree.insert("", "end", values=item1)

   def getImage(self):
        if self.mModels is not None:
            fields = ['name','list_price','image_1920']
            limit = 100
            global mo_list
            mo_list = self.mModels.execute_kw(self.mErpDB,self.mUser_id,self.mErpPwd,
                'product.template','search_read',
                [],
                {'fields': fields, 'limit': limit})
            for mo_dico in mo_list:
                print(f'----------------------------')
                #display_resized_image_in_tkinter(mo_dico['image_1920'])
                for k in mo_dico.keys():
                    print(f' - {k} : {mo_dico[k]}')


     #=====BOUTON DE VALIDATION SAISIE STOK=====
                
   def validate_entry(self): 
         
      ModifStok = self.AjoutProd.get()
    
      if ModifStok.isdigit():
         # Fonction appelée lors de la validation du bouton
         ifOdoo.getFields()
         data = []
         data = ifOdoo.getArticle()
         prod_app.add_data_to_table(data)

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
        ifOdoo.getFields()
        data = []
        data = ifOdoo.getArticle()
        prod_app.add_data_to_table(data)
        
            # Efface la saisie AjoutProd après la validation
        self.AjoutProd.delete(0, 'end')

         #Efface l'erreur de saisie 
        prod_labelerror.grid_forget()
    
   def BP1(self):
        print(Image1)
   def BP2(self):
        print(Image2)
   def BP3(self):
        print(Image3)
   def BP4(self):
        print(Image4)


if __name__ == "__main__":
    # Création de la fenêtre de connection
    #global prod_page
    #global connection_page
    #sdfghjk
    

    ifOdoo = IF_ErpOdoo("172.31.10.188", "8069","amaDB", "admin", "adminpython2024")
    if ifOdoo.connect():
        ifOdoo.getFields()
        data = []
        data = ifOdoo.getImage()

    connection_page = tk.Tk()
    
    # Création de la fenêtre principale + mettre invisible
    prod_page = tk.Tk()
    prod_page.withdraw()
    prod_app = Application(prod_page,connection_page)
    connection_app = Connection(connection_page,prod_page, prod_app) 
    
    #ceci est un commentaire
    # Loop des fenetres
    connection_page.mainloop()
    prod_page.mainloop()
    