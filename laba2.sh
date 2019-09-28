#!/bin/bash
#Запускать скрипт с sudo
#Установка go
wget "https://dl.google.com/go/go1.13.1.linux-amd64.tar.gz"
tar -C /usr/local -xzf go1.13.1.linux-amd64.tar.gz 
export PATH=$PATH:/usr/local/go/bin
export PATH=$PATH:$GOPATH/bin
source $HOME/.profile

#Установка git
apt install git 

#Скачивание репозитория
git clone https://github.com/yggdrasil-network/yggdrasil-go

#Установка Yggdrasil
cd yggdrasil-go
./build

