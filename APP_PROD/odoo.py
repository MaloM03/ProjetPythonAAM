import xmlrpc.client

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
