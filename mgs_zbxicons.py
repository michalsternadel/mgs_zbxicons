#!/usr/bin/env python3
# -*- coding: UTF8 -*-
# mgs_zbxicons.py
# Purpose: Generating icons with statuses for zabbix maps usage.
# Version: 0.0.3
# Date: 2021-03-19
# Author: Michal Sternadel <michal@sternadel.pl>
# Licence: GPLv2

# mgs_zbxicons.py - Zabbix icons creator and automate installer
# Copyright (C) 2018-2021 Michal Sternadel <michal@sternadel.pl>
#
# mgs_zbxicons.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# later version.

# mgs_zbxicons.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with mgs_zbxicons.py.  If not, see <http://www.gnu.org/licenses/>.

import os
from binascii import hexlify
from PIL import Image
sizes = [
 '128, 128',
 '96, 96',
 '64, 64',
 '48, 48',
 '24, 24']

if not os.path.exists('sql'):
    os.makedirs('sql')
if not os.path.exists('output'):
    os.makedirs('output')

mysqlFile = open('sql/mgs_zbxicons-mysql.sql','w')
mysqlFile.write("-- Zabbix MgS_Icons (c) Sternadel Michał 2021\n\r")
psqlFile = open('sql/mgs_zbxicons-psql.sql','w')
psqlFile.write("-- Zabbix MgS_Icons (c) Sternadel Michał 2021\n\r")


for icon in os.listdir('icons'):
	i = Image.open('icons/'+icon)
	#iwidth, iheight = i.size
	for tsize in sizes:
		tw,th=tsize.split(',')
		i = i.resize((int(tw),int(th)), Image.ANTIALIAS)
		iwidth, iheight = i.size
		i.save('output/'+icon.replace('.png', '_(')+str(iwidth)+').png')
		with open('output/'+icon.replace('.png', '_(')+str(iwidth)+').png', 'rb') as f:
			hexdata = str(hexlify(f.read())).replace("'",'')[1:] #, "utf-8")
			mysqlFile.write("insert into images (imageid, imagetype, name, image) SELECT COALESCE(MAX(imageid),0)+1, '1', '"+icon.replace('.png','')+"_("+str(iwidth)+")', x'"+hexdata+"' FROM images ON DUPLICATE KEY update image=x'"+hexdata+"';\n\r")
			psqlFile.write("insert into images (imageid, imagetype, name, image) SELECT COALESCE(MAX(imageid),0)+1, '1', '"+icon.replace('.png','')+"_("+str(iwidth)+")', DECODE('"+hexdata+"', 'hex') FROM images ON CONFLICT (name) DO UPDATE SET image=DECODE('"+hexdata+"', 'hex');\n\r")
		f.close()
	i.close()
for icon in os.listdir('icons'):
	for status in os.listdir('statuses'):
		i = Image.open('icons/'+icon)
		if status.replace('.png','') == 'DISABLED':
			i=i.convert('LA')
		iwidth, iheight = i.size
		s = Image.open('statuses/'+status)
		swidth, sheight = s.size
		i.paste(s, (iwidth-swidth,0), s)
		s.close()
		for tsize in sizes:
			tw,th=tsize.split(',')
			i = i.resize((int(tw),int(th)), Image.ANTIALIAS)
			iwidth, iheight = i.size
			i.save('output/'+icon.replace('.png', '')+'-'+status.replace('.png','_(')+str(iwidth)+').png')
			with open('output/'+icon.replace('.png', '')+'-'+status.replace('.png','_(')+str(iwidth)+').png', 'rb') as f:
				hexdata = str(hexlify(f.read())).replace("'",'')[1:] #, "utf-8")
				mysqlFile.write("insert into images (imageid, imagetype, name, image) SELECT COALESCE(MAX(imageid),0)+1, '1', '"+icon.replace('.png','')+"-"+status.replace('.png','')+"_("+str(iwidth)+")', x'"+hexdata+"' FROM images ON DUPLICATE KEY update image=x'"+hexdata+"';\n\r")
				psqlFile.write("insert into images (imageid, imagetype, name, image) SELECT COALESCE(MAX(imageid),0)+1, '1', '"+icon.replace('.png','')+"-"+status.replace('.png','')+"_("+str(iwidth)+")', DECODE('"+hexdata+"', 'hex') FROM images ON CONFLICT (name) DO UPDATE SET image=DECODE('"+hexdata+"', 'hex');\n\r")
			f.close()
		i.close()

mysqlFile.write("update ids set nextid=(SELECT max(imageid)+1 from images) where table_name='images';")
mysqlFile.close()
psqlFile.write("update ids set nextid=(SELECT max(imageid)+1 from images) where table_name='images';")
psqlFile.close()
