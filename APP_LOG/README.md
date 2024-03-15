-------------------------------------------------------------
-------------------------------------------------------------

## __METHODE 1__ (Automatique)
- Installer le dossier d'installe sur le bureau
- Ouvrir login_app.py dans le dossier log avec Bloc-notes pour modifier l'adresse IP
- Mettre la bonne adresse IP Oddo ligne 59 (adresse IP de la machine physique du serveur odoo)

- Lancer le fichier Setup_log avec la commande cmd ./bash setup_log.sh
  chemaind'accès : C:\Users\UIMM\Desktop\ProjetPythonAAM-main\APP_LOG\setup_log.sh
- Accepter le pare-feu

- Après l'installation lancer le fichier launcher_log.sh avec la commande ./bash launcher_log.sh

-------------------------------------------------------------
-------------------------------------------------------------
## __METHODE 2__ (Manuel)

## 1 / __installer le dossier d'installe sur le bureau__

## 2 / Instalation Python
__Aller dans la console et entrer ces commandes__   

```bash
sudo apt update
```
```bash
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev git
```
```bash
wget https://www.python.org/ftp/python/3.9.2/Python-3.9.2.tgz
```
```bash
tar -xf Python-3.9.2.tgz
```
```bash
cd Python-3.9.2
```
```bash
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall
```
```bash
cd ..
```
```bash
rm -rf Python-3.9.2 Python-3.9.2.tgz
```

## 3 / Installer PILLOW
```bash
sudo apt-get install python3-pil.imagetk
```

## 4 / Changer l'IP
- Ouvrire login_app  avec Bloc-notes

- Mettre la bonne adresse IP Oddo ligne 59 (adresse IP de la machine physique du serveur odoo)

## 5 / Lancer l'application production
__Aller dans la console et entrer ces commandes__      

```bash
cd /home/user/Bureau/Dos_python_del_mama/ProjetPythonAAM/APPP_LOG/
```
```bash
python3 main.py
```
-------------------------------------------------------------
-------------------------------------------------------------
