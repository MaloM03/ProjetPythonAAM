import xmlrpc.client
import tkinter as tk
from tkinter import ttk
import center_tk_window

#pour image
import base64
from io import BytesIO
from PIL import Image
from PIL import ImageTk


#=====PAGE D'APPLICATION=====
class Application : 
    
  #=====CREATION DE LA PAGE APPLICATION===== 
    def __init__(self, log_page, user_name):
      self.selected_id = None
      self.logistique = log_page
      self.logistique.title("AMA - Application Logistique")
        # Définir la taille initiale de la fenêtre
      #self.logistique.geometry("1000x300+500+300")
      self.logistique.geometry("1500x600+800+400")
      
      self.AjoutProd = tk.Entry(self.logistique)
        

      # Création des widgets pour l'interface utilisateur
      self.create_widgets()
        
    def set_odoo(self, currentOdoo):
        self.odooRef = currentOdoo
        
     #===== TABLEAU PRODUITS =====
    def create_widgets(self):

      # Création du Treeview (tableau)
      self.tree = ttk.Treeview(self.logistique, columns=("Nom", "Quantité de stok", "Prix àl'unité", "Code article"))

        # Configuration des colonnes
        
      self.tree.heading("Nom", text="Nom")
      self.tree.heading("Quantité de stok", text="Quantité de stok")
      self.tree.heading("Prix àl'unité", text="Prix unitaire €")
      #self.tree.heading("Image de ref", text="Image article")
      self.tree.heading("Code article", text="Code article")

      self.tree.bind('<<TreeviewSelect>>', self.on_select) #lier la fonction on_select a la selection de ligne dans le tableau


      # Ajout des données au tableau
      #self.add_data_to_table()
      #self.transform_data()
        
        

      # Affichage du tableau
      self.tree.grid(row=0, column=0, sticky="nsew")
        

      # Configuration du redimensionnement de la fenêtre
      self.logistique.grid_rowconfigure(0, weight=1)
      self.logistique.grid_columnconfigure(0, weight=1)

      #center_tk_window.center_on_screen(self.logistique)

      # Suppression de la colonne d'ID
      self.tree.column("#0", width=0, stretch=tk.NO)

     #===== SAISIE DE L'AJOUT DE PRODUCTION=====
        # Ajout du label sous le tableau
      prod_label = tk.Label(self.logistique, text="Modifier le stock de l'article sélectionné :")
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

      # Ajout du bouton voir image
      Photo_BP = tk.Button(self.logistique, text="Voir l'image de l'article", command=self.DisplayImage)
      Photo_BP.grid(row=5, column=0, sticky="w", padx=5, pady=5)

     #=====AFFICHAGE DU TABLEAU DES PRODUITS===== 
    def add_data_to_table(self, dataA, dataB):
      data = []

      for mo_dico in dataA :
         Article = 0
         OF = mo_dico['qty_available']
         QAP = " €" #mo_dico['product_qty']
         QDP = 0
         DATE = 2 #mo_dico['date_planned_start']
         ligne = (Article, OF,(QDP, "/" ,QAP), DATE)
         data.append(ligne)
      
      i=0

      for mo_dico in dataB :
         article, of, (qdp, _, qap), date = data[i]
         
         # Modifier les données spécifiques
         article = mo_dico['name']
         qdp = mo_dico['list_price']
         #qap = "NewQAP" + str(i)
         date = mo_dico['default_code']
         
         # Mettre à jour la liste
         data[i] = (article, of, (qdp), date)
         i = i + 1

         # Efface toutes les lignes actuelles du tableau
         for item in self.tree.get_children():
           self.tree.delete(item)
         #Apres avoir effacé on re - affiche le tableau modifié 
         for item1 in data:
            self.tree.insert("", "end", values=item1)

     #=====BOUTON DE VALIDATION SAISIE STOK=====

    def on_select(self, event):
        # Récupère l'élément sélectionné dans le tableau
        selected_item = self.tree.selection()

        # Vérifie si un élément est effectivement sélectionné
        if selected_item:
            # Récupère les valeurs des colonnes de l'élément sélectionné
            values = self.tree.item(selected_item)['values']
            self.selectedID = values[3]
            print("Éléments sélectionnés:", self.selectedID)

            # Extrait le nombre de la chaîne "WH/MO/00006"
            #self.selected_id = self.extract_number(values[1])
            #print("Numéro extrait:", self.selected_id)    
            
    def validate_entry(self):

      valeur = self.AjoutProd.get()
      if valeur.isdigit(): # La valeur est un entier
        print("pass entier")
        if self.selectedID is not None:
          self.odooRef.update_stock_quantity_by_default_code(self.selectedID,valeur)
          print("Modified ID :")
          print(self.selectedID)
          print("Valeur emise : ")
          print(valeur)
          self.refresh()
          self.effacer_ajout_prod()
          self.selected_id = None
      else:
         print("la valeur n'est pas un entier")
         self.effacer_ajout_prod()

      '''
      if ModifStok.isdigit():
         # Fonction appelée lors de la validation du bouton
         self.add_data_to_table()

         # Efface la saisie AjoutProd après la validation
         self.AjoutProd.delete(0, 'end')

         #Efface l'erreur de saisie 
         prod_labelerror.grid_forget()

      else: 
         prod_labelerror.grid(row=4, column=0)

         # Efface la saisie AjoutProd après la validation
         self.AjoutProd.delete(0, 'end')'''
    
    
    def refresh(self):

#Actualiser le tableau après une modification
          # Fonction appelée lors de la validation du bouton
      self.odooRef.getFields()
      dataA = self.odooRef.getArticle()
      dataB = self.odooRef.getImage()
      self.add_data_to_table(dataA, dataB)
      self.effacer_ajout_prod()
            
            # Efface la saisie AjoutProd après la validation
      #self.AjoutProd.delete(0, 'end')

         #Efface l'erreur de saisie 
      #prod_labelerror.grid_forget()
    def effacer_ajout_prod(self):
        """Fonction pour effacer le contenu de la zone de saisie 'AjoutProd'."""
        self.AjoutProd.delete(0, tk.END)

    def DisplayImage(self):
       ImageEnBase64 = self.odooRef.get_image_by_default_code(self.selectedID)
       self.display_resized_image_article(ImageEnBase64)

    def display_resized_image_article(self,encoded_string, width=256, height=256):
        # Décode la chaîne base64
        decoded_bytes = base64.b64decode(encoded_string)
        
        # Crée une image à partir des données décodées
        original_image = Image.open(BytesIO(decoded_bytes))
        # Redimensionne l'image
        resized_image = original_image.resize((width, height))

        # Crée une fenêtre Tkinter
        root = tk.Tk()
        root.title("Visualisation de l'image")

        # Convertit l'image redimensionnée en format Tkinter
        global tk_image
        tk_image = ImageTk.PhotoImage(resized_image)

        # Crée un widget Label pour afficher l'image
        label = tk.Label(root, image=tk_image)
        label.pack()

        # Lance la boucle principale Tkinter
        root.mainloop()
