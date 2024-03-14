#!/bin/bash


sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev git
wget https://www.python.org/ftp/python/3.9.2/Python-3.9.2.tgz
tar -xf Python-3.9.2.tgz
cd Python-3.9.2
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall
cd ..
rm -rf Python-3.9.2 Python-3.9.2.tgz
sudo apt-get install python3-pil.imagetk


