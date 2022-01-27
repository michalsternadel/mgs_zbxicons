# mgs_zbxicons
## _Zabbix maps icon generator._

Tool for generating icon pack to use with Zabbix maps.
It simply combines all png's from icons directory with all png files from status directory (default statuses are: DISABLED, ERROR, MAINTENANCE, OK) and saves them in output directory.
Can be installed by-hand or using generated SQL scripts on sql directory.

This repository includes some Tango-styled icons.

![Example map](https://raw.githubusercontent.com/michalsternadel/mgs_zbxicons/master/example_map.png)

# Installation

1. mgs_zbxicons requires python3 with pillow libraries (PIL), install it with pip or your package manager
```sh
pip3 install -r requirements.txt
```
2. Put your icons to "icons" directory or use already provided. Filename (without png extensions) will preserve as Drop-down names of icon.
3. Put your statuses to "statuses" directory.
4. Check usage and all available options:
```sh
python3 ./mgs_zbxicons -h
```
5. To generate icons and sql scripts run:
a) For mysql/mariadb backend:
```sh
python3 ./mgs_zbxicons.py -e mysql
```
b) For posgresql backend:
```sh
python3 ./mysql_zbxicons.py -e psql
```
6. Transfer _mgs_zbxicons-mysql.sql_ or _mgs_zbxicons-psql.sql_ to you zabbix mysql/postgresql server.
7. Import generated sql files to database engine:
a) For mysql/mariadb backend:
```sh
mysql -u zabbix_user -h zabbix_dbhost -p zabbix_db < ./mgs_zbxicons-mysql.sql
```
b) For postgresql backend:
```sh
psql -h zabbix_dbhost -U zabbix_user zabbix_db -f mgs_zbxicons-psql.sql
```

# Updating

Procedure is the same as instalation procedure.
