
#!/usr/bin/env python3
#=================================================================
# Interface ODOO avec l'API XML-RPC
#-----------------------------------------------------------------
# https://www.odoo.com/documentation/15.0/developer/misc/api/odoo.html
# Accéder à l'interface Web Odoo en mode debug => localhost:8069/web?debug=1
#=================================================================
import xmlrpc.client
#=================================================================
def fonction():

#=================================================================
if __name__ == "__main__":
fonction()
#=================================================================
def connect(erp_ipaddr, erp_port):
erp_url = f'http://{erp_ipaddr}:{erp_port}'
print("Connexion ODOO")
print(f"@URL={erp_url}")
try:
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(erp_url))
version = common.version()
print(f"Odoo version={version['server_serie']}")
except ConnectionRefusedError:
print("Odoo Server not found or connection rejected")
else:
global gUser_id
gUser_id = common.authenticate(gErp_db, gErp_user, gErp_pwd, {})
print(f"Odoo authentification:{gUser_id}")
if(gUser_id!=False):
global gModels
gModels = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(erp_url))
#=================================================================
if __name__ == "__main__":
connect("172.31.10.171", "8069")
if(user_id!=False):
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(erp_url))
access = models.execute_kw(erp_db, user_id, erp_pwd,
'mrp.production', 'check_access_rights',
['write'], {'raise_exception': False})
print(f"Manufactoring Order write access rights : {access}")
listing = models.execute_kw(erp_db, user_id, erp_pwd,
'mrp.production', 'fields_get',
[], {'attributes': []})
for attr in listing:
print(f' - {attr}')
else:
print(f'Odoo Server authentification rejected : DB={erp_db} User={erp_user}')
Programmation structurée 4/8
#-----------------------------------------------------------------
def getFields():
listing = gModels.execute_kw(gErp_db, gUser_id, gErp_pwd,
'mrp.production', 'fields_get',
[], {'attributes': []})
for attr in listing:
print(f' - {attr}')
#=================================================================
if __name__ == "__main__":
connect("172.31.10.171", "8069")
getFields()
erp_url = ""
erp_db = "amaDB"
erp_user = "inter"
erp_pwd = "inter"
#=================================================================
def connect(erp_ipaddr, erp_port):
global erp_url
erp_url = f'http://{erp_ipaddr}:{erp_port}'
print("Connexion ODOO")
print(f"@URL={erp_url}")
try:
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(erp_url))
version = common.version()

#=================================================================
#Exploitation de la base de données
#=================================================================
def getManufOrderToDo():
fields =['name', 'date_planned_start', 'product_id', 'product_qty', 'qty_producing', 'state']
limit = 10
mo_list = gModels.execute_kw(gErp_db, gUser_id, gErp_pwd,
'mrp.production', 'search_read',
[[('state', '=', 'confirmed'), ('qty_produced', '!=', 'product_qty')]],
{'fields': fields, 'limit': limit})
for mo_dico in mo_list:
print(f'----------------------------')
for k in mo_dico.keys():
print(f' - {k} : {mo_dico[k]}')

#=================================================================
#Programmation objet
#=================================================================
class IF_ErpOdoo:
"Classe objet d'interface de l'ERP Odoo en XML-RPC"
def __init__(self, erp_ipaddr, erp_port):
"Methode Constructeur de Classe"
print("##IF_ErpOdoo Constructor##")
self.mErpIpAddr = erp_ipaddr
self.mErpIpPort = erp_port
def __del__(self):
"Methode Constructeur de Classe"
print("##IF_ErpOdoo Destructor##")
def connect(self):
"Methode de connexion à l'ERP Odoo"
erp_url = f'http://{self.mErpIpAddr}:{self.mErpIpPort}'
print("Connexion ODOO")
print(f"@URL={erp_url}")
#=================================================================
if __name__ == "__main__":
ifOdoo = IF_ErpOdoo("172.31.10.171", "8069")
ifOdoo.connect()
#=================================================================
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
#=================================================================
if __name__ == "__main__":
ifOdoo = IF_ErpOdoo("172.31.10.171", "8069", "amaDB", "inter", "inter")
ifOdoo.connect()
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
mo_list = self.mModels.execute_kw(self.mErpDB, self.mUser_id, self.mErpPwd,
'mrp.production', 'search_read',
[[('state', '=', 'confirmed'), ('qty_produced', '!=', 'product_qty')]],
{'fields': fields, 'limit': limit})
for mo_dico in mo_list:
print(f'----------------------------')
for k in mo_dico.keys():
print(f' - {k} : {mo_dico[k]}')
#=================================================================
if __name__ == "__main__":
ifOdoo = IF_ErpOdoo("192.168.0.17", "8069", "vitre", "inter", "inter")
ifOdoo.connect()
ifOdoo.getFields()
ifOdoo.getManufOrderToDo()
#=================================================================
#Re init de la classe d'interface Odoo
#=================================================================
def __init__(self, erp_ipaddr, erp_port, erp_db, erp_user, erp_pwd):
"""Methode Constructeur de Classe"""
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
def setServer(self, erp_ipaddr, erp_port):
self.mErpIpAddr = erp_ipaddr
self.mErpIpPort = erp_port
self.connect()
if __name__ == "__main__":
ifOdoo = IF_Odoo("192.168.0.17", "8066", "vitre", "inter", "inter")
ifOdoo.connect()
print(f'=> Version : {ifOdoo.mOdooVersion}')
ifOdoo.setServer("172.31.10.171", "8069")
print(f'=> Version : {ifOdoo.mOdooVersion}')
#=================================================================
#Extension de la classe d'interface Odoo
#=================================================================
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
f __name__ == "__main__":
ifOdoo = IF_Odoo("192.168.0.17", "8066", "vitre", "inter", "inter")
ifOdoo.connect()
print(f'=> Version : {ifOdoo.mOdooVersion}')
ifOdoo.setServer("192.168.0.17", "8069")
ifOdoo.connect()
print(f'=> Version : {ifOdoo.mOdooVersion}')
ifOdoo.getFields('mrp.bom')
print(ifOdoo.mListFields)
ifOdoo.getFields()
ifOdoo.printFields()