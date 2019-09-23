# mgs_zbxicons
Zabbix maps icon generator.

Tool for generating icon pack to use with Zabbix maps.
It simply combines all png's from icons with all png's from status (default: DISABLED, ERROR, MAINTENANCE, OK) and saves them in output directory.
Easy to install and update sql scripts are generated at sql directory.

This repository includes some Tango-styled icons.

![Example map](https://raw.githubusercontent.com/michalsternadel/mgs_zbxicons/master/example_map.png)

# Installation

1. Put your icons to "icons" directory. Filename (without png extensions) will preserve as Drop-down names of icons.
2. Put your statuses to "statuses" directory.
3. Run python ./mgs_zbxicons.py
4. Transfer upgrade.sql to you zabbix mysql server.
5. execute mysql -u root -p [your_zabbix_database] < ./upgrade.sql

# Updating

Procedure is the same as above (Instalation procedure)

