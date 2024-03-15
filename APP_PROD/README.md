----------------------------------------------------------------------------------
----------------------------------------------------------------------------------
## __METHODE 1__ (Automatique)
- Mettre le dossier d'installation sur le bureau (APP PRODUCTION)  
- Ouvrir login_app.py dans le dossier prod avec Bloc-notes pour modifier l'adresse IP  
- Mettre la bonne adresse IP d'Odoo à la ligne 55 (adresse IP de la machine physique du serveur odoo)  
- Ouvrez un terminal à l'emplacement du dossier  
- Lancer le fichier setup_prod.bat en double cliquant sur celui-ci  
- Après l'installation lancer le fichier launcher_prod.bat en double cliquant sur celui-ci   

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
