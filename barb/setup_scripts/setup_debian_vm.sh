#!/usr/bin/env bash

# Update Python to 3.7, and set it as the default

# Install debian dependancies
sudo apt-get -y install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget libbz2-dev lzma-dev liblzma-dev

# Install python3.7 and delete it
wget https://www.python.org/ftp/python/3.7.5/Python-3.7.5.tgz
tar xvf Python-3.7.5.tgz
cd Python-3.7.5
sudo ./configure #--enable-shared LDFLAGS="-Wl,--rpath=/usr/bin/lib"
sudo make -j16
sudo make install
cd ..
rm Python-3.7.5.tgz
sudo rm -rf Python-3.7.5/


# Debian software

sudo apt-get install -y htop
sudo apt-get install -y vim
