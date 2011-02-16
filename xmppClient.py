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

class xmppClient:
	connected = False
	mucs = {}

	validHandlerNames = ['message', 'presence']

	def __init__(self, jid, password, debug=[]):
		jid = xmpp.JID(jid)
		self.user = jid.getNode()
		self.server = jid.getDomain()
		self.password = password

		self.client = xmpp.Client(self.server, debug=debug)
		res = self.client.connect()

		if not res:
			print "Error connecting to server: " + self.server
			return

		res = self.client.auth(self.user, self.password)

		if not res:
			print "Error authenticating user: " + self.user
			return

		self.client.sendInitPresence()

	def disconnect(self):
		self.client.disconnect()

	def isConnected(self):
		return self.client.isConnected()

	def joinMUC(self, nick, muc, password=''):
		presence = xmpp.Presence(to=muc + '/' + nick)
		presence.setTag('x', namespace=xmpp.NS_MUC).setTagData('password', password)
		presence.getTag('x').addChild('history', {'maxchars': '0', 'maxstanzas': '0'});
		self.client.send(presence)

	def sendMessage(self, jid, message, type='chat'):
		message = xmpp.protocol.Message(to=jid, body=message, typ=type)
		self.client.send(message)

	def step(self):
		try:
			self.client.Process(0.1)
		except KeyboardInterrupt:
			return 0
		return 1

	def getMUC(self, name):
		if name in self.mucs:
			return self.mucs[name]

	def registerHandler(self, name, handler):
		if name in self.validHandlerNames:
			self.client.RegisterHandler(name, handler)
		else:
			raise ValueError()