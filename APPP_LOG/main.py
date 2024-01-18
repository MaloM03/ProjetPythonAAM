from login_app import *
from odoo import *
from log_app import *

if __name__ == "__main__":
    # Création de la fenêtre de connection
    #global prod_page
    #global connection_page
    connection_page = tk.Tk()
    
    # Création de la fenêtre principale + mettre invisible
    log_page = tk.Tk()
    log_page.withdraw()
    log_app = Application(log_page,connection_page)
    connection_app = Connection(connection_page,log_page, log_app) 
    
    #ceci est un commentaire
    # Loop des fenetres
    connection_page.mainloop()
    log_page.mainloop()
    