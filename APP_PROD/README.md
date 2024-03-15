----------------------------------------------------------------------------------
----------------------------------------------------------------------------------
## __METHODE 1__ (Automatique)
- Installer le dossier d'installe sur le Bureau
- Ouvrir login_app du dossier PROD avec Bloc-notes 
- Mettre la bonne adresse IP d'Odoo à la ligne 55

- Lancer le fichier Setup_prod  
  chemaind'accès : C:\Users\UIMM\Desktop\ProjetPythonAAM-main\APP_PROD\setup_prod.bat
- Accepter le pare-feu

----------------------------------------------------------------------------------
----------------------------------------------------------------------------------
## __METHODE 2__ (Manuel)

## 1 / Installer le dossier sur le Bureau

## 2 / Instalation Python
__Aller dans la console et entrer ces commandes__   

```bash
curl -O https://www.python.org/ftp/python/3.9.3/python-3.9.3-amd64.exe
```
```bash
python-3.9.3-amd64.exe
```
---------------------------------------------------------------------------------
__Cocher la case Add Python 3.9 to PATH__
---------------------------------------------------------------------------------

![Cocher la case Add Python 3.9 to PATH](Image_README/MicrosoftTeams-image-2.png)
----------------------------------------------------------------------------------
----------------------------------------------------------------------------------  
__Cliquer sur Install New__ 
---------------------------------------------------------------------------------

![Cliquer sur Install New](Image_README/MicrosoftTeams-image-2.png)
----------------------------------------------------------------------------------
----------------------------------------------------------------------------------  
Accepter le pare-feu

## 3 / Installer PILLOW
```bash
pip install pillow
```

## 4 / Changer l'IP
- Ouvrir login_app avec Bloc-notes  

- Mettre la bonne adresse IP d'Odoo à la ligne 55

## 5 / Lancer l'application production
__Aller dans la console et entrer ces commandes__   

```bash
\Users\UIMM\Desktop\ProjetPythonAAM-main\APP_PROD\main.py
```
----------------------------------------------------------------------------------
----------------------------------------------------------------------------------
