from login_app import *
from odoo import *
from prod_app import *

if __name__ == "__main__":
    # Création de la fenêtre de connection
    #global prod_page
    #global connection_page
    connection_page = tk.Tk()
    
    # Création de la fenêtre principale + mettre invisible
    prod_page = tk.Tk()
    prod_page.withdraw()
    connection_app = Connection(connection_page,prod_page) 
    prod_app = Application(prod_page,connection_page)
    
    # Loop des fenetres
    connection_page.mainloop()
    prod_page.mainloop()
    