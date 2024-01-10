from login_app import *
from odoo import *

if __name__ == "__main__":
    connection_page = tk.Tk()
    connection_app = Connection(connection_page)
    connection_page.mainloop() 
    