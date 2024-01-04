#!/usr/bin/env python3

#=================================================================
# Interface ODOO avec l'API XML-RPC
#-----------------------------------------------------------------
# https://www.odoo.com/documentation/15.0/developer/misc/api/odoo.html
# Accéder à l'interface Web Odoo en mode debug => localhost:8069/web?debug=1
#=================================================================

#=================================================================
import xmlrpc.client
#=================================================================

#=================================================================
def connect(erp_ipaddr, erp_port):
erp_url = f'http://{erp_ipaddr}:{erp_port}'

print("Connexion ODOO")
print(f"@URL={erp_url}")

try:
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(erp_url))
version = common.version()
print(f"Odoo version={version['server_serie']}")

#=================================================================

if __name__ == "__main__":
connect(172.31.10.171)