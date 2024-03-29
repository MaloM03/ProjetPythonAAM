import xmlrpc.client

# ===== PROGRAMME DE CONNECTION A ODOO ====

class IF_ErpOdoo:
    "Classe objet d'interface de l'ERP Odoo en XML-RPC"

    def __init__(self, erp_ipaddr, erp_port, erp_db, erp_user, erp_pwd):
        "Méthode Constructeur de Classe"
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
        "Méthode Destructeur de Classe"
        print("##IF_ErpOdoo Destructor##")

    def connect(self):
        """Méthode de connexion à l'ERP Odoo"""
        erp_url = f'http://{self.mErpIpAddr}:{self.mErpIpPort}'
        print("Connexion ODOO")
        print(f"@URL={erp_url}")

        # Connexion à Odoo
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

        if self.mUser_id != False:
            self.mModels = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(erp_url))
            access = self.mModels.execute_kw(self.mErpDB, self.mUser_id, self.mErpPwd,
                        'mrp.production', 'check_access_rights',
                        ['write'], {'raise_exception': False})
            
            print(f"Manufacturing Order write access rights : {access}")

            # Récupération des ordres de fabrication
            mo_list = self.getManufOrderToDo()
            """
            # Mise à jour de la quantité produite d'un ordre de fabrication (ex: ID 4 ) à 15
            order_id = 4
            new_qty_producing = 15

            result = self.update_manufacturing_order_qty_producing(order_id, new_qty_producing)

            if result:
                print(f"Quantité produite mise à jour pour l'ordre de fabrication {order_id}")
            else:
                print(f"Échec de la mise à jour de la quantité produite pour l'ordre de fabrication {order_id}")

            # Ajout de l'appel pour afficher les articles après la mise à jour
            self.getArticle()"""

            return True
        else:
            print(f'Odoo Server authentification rejected : DB={self.mErpDB} User={self.mErpUser}')
            return False

    def setServer(self, erp_ipaddr, erp_port):
        self.mErpIpAddr = erp_ipaddr
        self.mErpIpPort = erp_port
        self.connect()

    def getFields(self, base='mrp.production'):
        if self.mModels is not None:
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
        if self.mModels is not None:
            fields = ['id','name', 'date_planned_start', 'product_id', 'product_qty', 'qty_producing', 'create_date']
            limit = 10
            global mo_list
            mo_list = self.mModels.execute_kw(self.mErpDB, self.mUser_id, self.mErpPwd,
                    'mrp.production', 'search_read',[],
                    {'fields': fields, 'limit': limit})   
        
            
            for mo_dico in mo_list:
                print(f'----------------------------')
                for k in mo_dico.keys():
                    print(f' - {k} : {mo_dico[k]}')
            return mo_list

    def update_manufacturing_order_qty_producing(self, order_id, new_qty_producing):

        print("update lancé ici")
        #order_id = 2
        if self.mModels is not None:
            try:
                # Effectuez la mise à jour de la quantité produite de l'ordre de fabrication
                self.mModels.execute_kw(self.mErpDB, self.mUser_id, self.mErpPwd,
                        'mrp.production', 'write',[[order_id], {'qty_producing': new_qty_producing}])

                return True
                print("write do")
            except xmlrpc.client.Fault as e:
                print(f"Erreur lors de la mise à jour de la quantité produite de l'ordre de fabrication : {e}")
                return False
        else:
            print("Veuillez d'abord vous connecter à Odoo.")
            return False
        print("fin de la function")

    def getArticle(self):
        """
        Affiche les articles après la mise à jour.
        """
        if self.mModels is not None:
            try:
                # Remplacez 'product.product' par le nom réel du modèle des articles dans votre instance Odoo
                articles = self.mModels.execute_kw(self.mErpDB, self.mUser_id, self.mErpPwd,
                        'product.product', 'search_read',
                        [[]],
                        {'fields': ['name', 'qty_available', 'virtual_available']})

                print("Articles après la mise à jour :")
                for article in articles:
                    print(f"Nom: {article['name']}, Quantité disponible: {article['qty_available']}, Quantité virtuelle disponible: {article['virtual_available']}")

            except xmlrpc.client.Fault as e:
                print(f"Erreur lors de la récupération des articles : {e}")
        else:
            print("Veuillez d'abord vous connecter à Odoo.")
        pass

# Exemple d'utilisation
#obj = IF_ErpOdoo('172.31.10.188', '8069', 'amaDB', 'a', 'a')
#obj.setServer('172.31.10.188', '8069')
