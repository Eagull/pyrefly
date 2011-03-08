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

import xmpp

def joinMUC(client, nick, muc, password=''):
	presence = xmpp.Presence(to=muc + '/' + nick)
	presence.setTag('x', namespace=xmpp.NS_MUC).setTagData('password', password)
	presence.getTag('x').addChild('history', {'maxchars': '0', 'maxstanzas': '0'});
	client.send(presence)

def sendMessage(client, jid, message, type='chat'):
	message = xmpp.protocol.Message(to=jid, body=message, typ=type)
	client.send(message)

def step(client):
	try:
		client.Process(0.1)
	except KeyboardInterrupt:
		return 0
	return 1