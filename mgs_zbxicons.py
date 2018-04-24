#!/usr/bin/python
# mgs_zbxicons.py
# Purpose: Generating icons with statuses for zabbix maps usage.
# Version: 0.0.1
# Date: 2018-04-24
# Author: Michal Sternadel <michal@sternadel.pl>
# Licence: GPLv2

# mgs_zbxicons.py - Zabbix icons creator and automate installer
# Copyright (C) 2018 Michal Sternadel <michal@sternadel>
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

insertFile = open('sql/insert.sql','w')
insertFile.write("-- Zabbix MgS_Icons (c) Sternadel Michał 2018\n\r")
updateFile = open('sql/update.sql','w')
updateFile.write("-- Zabbix MgS_Icons (c) Sternadel Michał 2018\n\r")
upgradeFile = open('sql/upgrade.sql','w')
upgradeFile.write("-- Zabbix MgS_Icons (c) Sternadel Michał 2018\n\r")
fixFile = open('sql/fix.sql','w')
fixFile.write("-- Zabbix MgS_Icons (c) Sternadel Michał 2018\n\r")


for icon in os.listdir('icons'):
	i = Image.open('icons/'+icon)
	#iwidth, iheight = i.size
	for tsize in sizes:
		tw,th=tsize.split(',')
		i = i.resize((int(tw),int(th)), Image.ANTIALIAS)
		iwidth, iheight = i.size
		i.save('output/'+icon.replace('.png', '_(')+str(iwidth)+').png')
		with open('output/'+icon.replace('.png', '_(')+str(iwidth)+').png', 'rb') as f:
			hexdata = (str(hexlify(f.read()), "utf-8"))
			insertFile.write("insert into images (imageid, imagetype, name, image) SELECT COALESCE(MAX(imageid),0)+1, '1', '"+icon.replace('.png','')+"_("+str(iwidth)+")', x'"+hexdata+"' FROM images;\n\r")
			updateFile.write("update images set image=x'"+hexdata+"' where name='"+icon.replace('.png','')+"_("+str(iwidth)+")';\n\r")
			upgradeFile.write("insert into images (imageid, imagetype, name, image) SELECT COALESCE(MAX(imageid),0)+1, '1', '"+icon.replace('.png','')+"_("+str(iwidth)+")', x'"+hexdata+"' FROM images ON DUPLICATE KEY update image=x'"+hexdata+"';\n\r")
		f.close()
	i.close()
for icon in os.listdir('icons'):
	for status in os.listdir('statuses'):
		i = Image.open('icons/'+icon)
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
				hexdata = (str(hexlify(f.read()), "utf-8"))
				insertFile.write("insert into images (imageid, imagetype, name, image) SELECT COALESCE(MAX(imageid),0)+1, '1', '"+icon.replace('.png','')+"-"+status.replace('.png','')+"_("+str(iwidth)+")', x'"+hexdata+"' FROM images;\n\r")
				updateFile.write("update images set image=x'"+hexdata+"' where name='"+icon.replace('.png','')+"-"+status.replace('.png','')+"_("+str(iwidth)+")';\n\r")
				upgradeFile.write("insert into images (imageid, imagetype, name, image) SELECT COALESCE(MAX(imageid),0)+1, '1', '"+icon.replace('.png','')+"-"+status.replace('.png','')+"_("+str(iwidth)+")', x'"+hexdata+"' FROM images ON DUPLICATE KEY update image=x'"+hexdata+"';\n\r")
				fixFile.write("update images set name='"+icon.replace('.png','')+"-"+status.replace('.png','')+"_("+str(iwidth)+")' where name='"+icon.replace('.png','')+"-"+status+"_("+str(iwidth)+")';\n\r")
			f.close()
		i.close()

insertFile.close()
updateFile.close()
upgradeFile.close()
fixFile.close()