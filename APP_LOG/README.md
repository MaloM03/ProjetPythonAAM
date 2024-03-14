## 1 / Instalation Python
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

## 2 / Installer PILOW
```bash
sudo apt-get install python3-pil.imagetk
```

## 3 / Changer l'IP
- Ouvrire login_app  
  chemain d'acces : /home/user/Bureau/Dos_python_del_mama/ProjetPythonAAM/APPP_LOG/  

- Mettre la bonne adresse IP Oddo ligne 59

## 4 / Lancer l'application production
```bash
cd /home/user/Bureau/Dos_python_del_mama/ProjetPythonAAM/APPP_LOG/
```
```bash
python3 main.py
```
