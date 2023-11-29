#!/usr/bin/env python3
# -*- coding: UTF8 -*-
# mgs_zbxicons.py
# Purpose: Generating icons with statuses for zabbix maps usage.
# Version: 0.0.4
# Date: 2022-01-27
# Author: Michal Sternadel <michal@sternadel.pl>
# Licence: GPLv2

# mgs_zbxicons.py - Zabbix icons creator and automate installer
# Copyright (C) 2018-2022 Michal Sternadel <michal@sternadel.pl>
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
import sys
import argparse
from binascii import hexlify
from PIL import Image

def generate_icons(resolution, states):
	print('Generating icons...');
	sizes = [
	 '128, 128',
	 '96, 96',
	 '64, 64',
	 '48, 48',
	 '24, 24']

	if not os.path.exists('output'):
	    os.makedirs('output')

	for icon in os.listdir('icons'):
		i = Image.open('icons/'+icon)
		for tsize in sizes:
			if (resolution in tsize) or resolution == 'all':
				tw,th=tsize.split(',')
				i = i.resize((int(tw),int(th)), Image.Resampling.LANCZOS)
				iwidth, iheight = i.size
				i.save('output/'+icon.replace('.png', '_(')+str(iwidth)+').png')
		i.close()

	if (states=='all'):

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
					if (resolution in tsize) or resolution == 'all':
						tw,th=tsize.split(',')
						i = i.resize((int(tw),int(th)), Image.Resampling.LANCZOS)
						iwidth, iheight = i.size
						i.save('output/'+icon.replace('.png', '')+'-'+status.replace('.png','_(')+str(iwidth)+').png')
				i.close()

def generate_query(engine):
	print('Generating query...')
	if not os.path.exists('sql'):
	    os.makedirs('sql')
	if (engine=='mysql'):
		sqlFile = open('sql/mgs_zbxicons-mysql.sql','w', encoding='utf-8')
		sqlFile.write("-- Zabbix MgS_Icons (c) Sternadel Michał 2022\n\r")
	if (engine=='psql'):
		sqlFile = open('sql/mgs_zbxicons-psql.sql','w', encoding='utf-8')
		sqlFile.write("-- Zabbix MgS_Icons (c) Sternadel Michał 2022\n\r")
	
	for icon in os.listdir('output'):
		with open('output/'+icon, 'rb') as f:
			hexdata = str(hexlify(f.read())).replace("'",'')[1:] #, "utf-8")
			if (engine=='mysql'):
				sqlFile.write("insert into images (imageid, imagetype, name, image) SELECT COALESCE(MAX(imageid),0)+1, '1', '"+icon.replace('.png','')+"', x'"+hexdata+"' FROM images ON DUPLICATE KEY update image=x'"+hexdata+"';\n\r")
			if (engine=='psql'):
				sqlFile.write("insert into images (imageid, imagetype, name, image) SELECT COALESCE(MAX(imageid),0)+1, '1', '"+icon.replace('.png','')+"', DECODE('"+hexdata+"', 'hex') FROM images ON CONFLICT (name) DO UPDATE SET image=DECODE('"+hexdata+"', 'hex');\n\r")
		f.close()
	sqlFile.write("update ids set nextid=(SELECT max(imageid)+1 from images) where table_name='images';")
	sqlFile.close()
	
def flush_outputdir():
	print('Flushing output directory...')
	if os.path.exists('output'):
		for icon in os.listdir('output'):
			os.unlink('output/'+icon)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(__file__, description='mgs_zbxicons.py - Zabbix icons creator and automate installer')
	parser.add_argument('-e', '--engine', help='database engine. Options: [mysql, psql] Default: none')
	parser.add_argument('-s', '--states', help='states to generate. Options: [none, all] Default: none', default='none')
	parser.add_argument('-r', '--resolution', help='the size of the resulting icons. Options: [24, 48, 64, 96, 128, all] Default: all', default='all')
	parser.add_argument('-q', '--generatequery', help='generate sql query. Default: true', default=True)
	parser.add_argument('-f', '--flush', help='remove icons from output directory before operation. Default: false', action="store_true", default=False)
	args = parser.parse_args()
	if (args.engine and args.states and args.resolution):
		if(args.states not in ['none', 'all']):
			print('Error: Invalid state value.')
			sys.exit(1)
		if(args.resolution not in ['all', '24', '48', '64', '96', '128']):
			print('Error: Invalid resolution value.')
			sys.exit(1)
		if(args.flush == True):
			flush_outputdir()
		generate_icons(args.resolution, args.states)
		if (args.engine == 'mysql' or args.engine == 'psql'):
			if (args.generatequery):
				generate_query(args.engine)
		else:
			print('Error: Not suported database engine.')
			sys.exit(1)
		sys.exit(0)
	else:
		print('mgs_zbxicons.py - Zabbix icons creator and automate installer')
		print('Use -h, --help option for usage instructions')
		sys.exit(0)