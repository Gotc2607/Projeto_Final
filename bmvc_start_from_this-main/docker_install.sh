#!/bin/bash

# Script para instalar Docker e Vim no Ubuntu 20.04

# Verificar se o script está sendo executado como root
if [[ $EUID -ne 0 ]]; then
   echo "Este script precisa ser executado com permissões de superusuário (sudo)." 
   exit 1
fi

# Atualizar lista de pacotes
apt update

# Instalar dependências para usar repositório HTTPS e o Vim
apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common \
    vim

# Adicionar chave GPG oficial do Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

# Adicionar repositório Docker ao sistema
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Atualizar lista de pacotes com repositório Docker
apt update

# Instalar Docker
apt install -y docker-ce docker-ce-cli containerd.io

# Adicionar usuário atual ao grupo docker
usermod -aG docker $SUDO_USER

# Reiniciar serviço Docker para aplicar alterações
systemctl restart docker

# Verificar status do serviço Docker
systemctl status docker

