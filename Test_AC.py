import xmlrpc.client

erp_ipaddr = "172.31.10.171"
erp_port = "8069"
erp_url = f'http://{erp_ipaddr}:{erp_port}'
print("Connexion ODOO")
print(f"@URL={erp_url}")

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(erp_url))
version = common.version()
print(f"Odoo version={version}")
{version['server_serie']}

erp_db = "amaDB"
erp_user = "arthur.cadran@gmail.com"
erp_pwd = "aampython2024"
user_id = common.authenticate(erp_db, erp_user, erp_pwd, {})
print(f"Odoo authentification:{user_id}")