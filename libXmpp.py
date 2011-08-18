'''
XMPP Bot
Copyright (C) 2011 Eagull.net

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

from handler import Handler
from xmpp.protocol import NS_MUC_USER, Iq, NS_MUC_ADMIN, JID
import xmpp

class Client(object):

	def __init__(self, bot, strJid):
		self.bot = bot
		self.jid = xmpp.Jid(strJid)
		self.client = xmpp.Client(self.jid.getDomain(), debug=[])
		self.mucs = {}
	
	def connect(self, password, resource):
		res = self.client.connect()
		if not res:
			return (False, "Error connecting to server: %s" % jid.getDomain())
		
		res = self.client.auth(self.jid.getNode(), password, resource)
		if not res:
			return (False, "Error authenticating as %s" % self.jid.getNode())
		
		self.client.sendInitPresence()
		
		return (True)
	
	def join(self, mucName, nick, password=''):
		lMucName = mucName.lower()
		if lMucName in self.mucs:
			return self.mucs[lMucName]
		
		muc = Muc(self, name, nick)
		self.mucs[lMucName] = muc
		muc.sendPresence(password)
		
		return muc
		
class Muc(object):

	def __init__(self, client, name, nick):
		self.name = name
		self.nick = nick
		self.manager = manager
		self.bot = bot
		
		self.roomId = "%s/%s" % (name, nick)
	
	def sendPresence(self, password):
		presence = xmpp.Presence(to=self.roomId)
		x = presence.setTag('x', namespace=xmpp.NS_MUC)
		x.setTagData('password', password)
		x.addChild('history', {'maxchars': '0', 'maxstanzas': '0'});

		self.client.client.sendPresence(presence)
		
class User(object):
	
	def __init__(self, muc, nick):
		