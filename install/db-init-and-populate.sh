#!/bin/bash

# Reset local DB

echo "Création base de données + utilisateurs"
sudo mysql -e "DROP DATABASE yackunivdb;"
sudo mysql -e "CREATE DATABASE yackunivdb;"
sudo mysql -e "CREATE USER 'admin_yackuniv'@'localhost' IDENTIFIED BY 'YackUnivDbPass';FLUSH PRIVILEGES;"
sudo mysql -e "GRANT ALL PRIVILEGES ON yackunivdb.* TO 'admin_yackuniv'@'localhost';FLUSH PRIVILEGES;"

echo "Initialisation de la base de données"
rm -r migrations

# Changed after Flask 2.0 transition
export FLASK_APP=app/yacka.py
export FLASK_ENV="local"
flask db init
flask db migrate
flask db upgrade

echo "Population de la base"
mysql -u admin_yackuniv -p'YackUnivDbPass' -D yackunivdb < install/yackunivdbdump.sql
