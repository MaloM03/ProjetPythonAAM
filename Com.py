#!/usr/bin/env python3

#=================================================================
# Interface ODOO avec l'API XML-RPC
#-----------------------------------------------------------------
# https://www.odoo.com/documentation/15.0/developer/misc/api/odoo.html
# Accéder à l'interface Web Odoo en mode debug => localhost:8069/web?debug=1
#=================================================================

import xmlrpc.client

gErp_db = "amaDB"
gErp_user = "admin"
gErp_pwd = "adminpython2024"

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
        print(f"Odoo Server not found or connection rejected")

    else:
        global gUser_id
        gUser_id = common.authenticate(gErp_db, gErp_user, gErp_pwd, {})
        print(f"Odoo authenfication:{gUser_id}")
    if(gUser_id!=False):
        global gModels
        gModels = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(erp_url))
#-----------------------------------------------------------------
    
def getFields():

    access = gModels.execute_kw(gErp_db, gUser_id, gErp_pwd,
        'mrp.production', 'check_access_rights',
        ['write'], {'raise_exception': False})
    print(f"Manufactoring Order write access rights : {access}")
    
    if(gUser_id!=False):
        listing = gModels.execute_kw(gErp_db, gUser_id, gErp_pwd,
            'mrp.production', 'fields_get',
            [], {'attributes': []})
        for attr in listing:
            print(f' - {attr}')

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

if __name__ == "__main__":
    connect("172.31.10.171","8069")
    getFields()
    getManufOrderToDo()