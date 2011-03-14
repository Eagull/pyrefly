'''
XMPP Bot
Copyright (C) 2011 Eagull.net

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import ConfigParser, hashlib

# parse config files
botConf = "bot.conf"

conf = ConfigParser.RawConfigParser()
conf.read(botConf)
sha1 = hashlib.sha1()
fp = open(botConf)
sha1.update(fp.read())
hash = sha1.hexdigest()
fp.close();

def get(option, section='default'):
	return conf.get(section, option)

def getRoomList():
	roomList = []
	for room in conf.sections():
		if '@' in room:
			roomList.append(room)
	return roomList

def set(option, value, section='default'):
	conf.set(section, option, value)
	fp = open(botConf, 'w')
	conf.write(fp)
	fp.close()