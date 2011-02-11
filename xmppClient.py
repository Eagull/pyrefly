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

class XMPPConnection:
	connected = False
	mucs = {}

	validHandlerTypes = {'message', 'presence'}

	def __init__(self, jid, password):
		jid = xmpp.JID(jid)
		self.user = jid.getNode()
		self.server = jid.getDomain()
		self.password = password

		self.client = xmpp.Client(self.server)
		res = self.client.connect()

		if not res:
			print "Error connecting to server: " + self.server
			return

		res = self.client.auth(self.user, self.password)

		if not res:
			print "Error authenticating user: " + self.user
			return

		self.client.RegisterHandler('message', self.messageHandler)
		self.client.RegisterHandler('presence', self.presenceHandler);

		self.client.sendInitPresence()

		self.connected = True

	def disconnect(self):
		self.client.disconnect()
		self.connected = False

	def isConnected(self):
		return self.connected

	def joinMUC(self, nick, muc, password=''):
		p = xmpp.Presence(to=muc + '/' + nick)
		p.setTag('x', namespace=xmpp.NS_MUC).setTagData('password', password)
		p.getTag('x').addChild('history', {'maxchars': '0', 'maxstanzas': '0'});
		self.client.send(p)

	def sendMessage(self, jid, message, tp='chat'):
		m = xmpp.protocol.Message(to=jid, body=message, typ=tp)
		self.client.send(m)

	def step(self):
		try:
			self.client.Process(0.1)
		except KeyboardInterrupt:
			return 0

		return 1

	def getMUC(self, name):
		if name in self.mucs:
			return self.mucs[name]

	def registerHandler(self, type, handler):
		if type in validHandlerTypes:
			self.client.RegisterHandler(type, handler)
		else:
			raise ValueError()