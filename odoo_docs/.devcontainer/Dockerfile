# Use the official Ubuntu image as a base
FROM mcr.microsoft.com/devcontainers/base:ubuntu


RUN apt-get update &&  apt-get install -y bash python3  python3-venv  python3-pip libldap2-dev libpq-dev libsasl2-dev postgresql-client
# install npm
# RUN apt-get install python3-pip libldap2-dev libpq-dev libsasl2-dev
# RUN  apt-get install -y libpq-dev


RUN apt install nodejs npm -y

Run npm install -g rtlcss




# Set up a default non-root user (VS Code devcontainers best practice)
# USER vscode
# WORKDIR /workspace
# WORKDIR /workspace
# 
