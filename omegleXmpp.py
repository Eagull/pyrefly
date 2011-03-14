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

from xmpp.protocol import Message, Presence
import config
import libomegle
import xmpp
from threading import Thread

class OmegleClient:
	nick = None
	isPublic = True
	targetHandle = None
	muc = None
	omegleClient = None
	xmppClient = None
	connected = False
	thread = None

	def __init__(self, muc, nick='Stranger'):
		jid = xmpp.JID(config.get("id", "omegle"))
		user = jid.getNode()
		server = jid.getDomain()
		password = config.get("password")
		self.nick = nick
		self.muc = muc
		self.xmppClient = xmpp.Client(server, debug=[]);
		connResult = self.xmppClient.connect()
		if not connResult: print "Error connecting to server: " + server
		connResult = self.xmppClient.auth(user, password, nick)
		if not connResult: print "Error authenticating user: " + user

		self.xmppClient.sendInitPresence()
		self.xmppClient.RegisterHandler('message', self.xmppMessageHandler)
		self.xmppClient.RegisterHandler('presence', self.xmppPresenceHandler)

		self.omegleClient = libomegle.Omegle()
		self.omegleClient.registerHook('join', self.omegleJoin)
		self.omegleClient.registerHook('leave', self.omegleLeave)
		self.omegleClient.registerHook('message', self.omegleMessage)
		self.omegleClient.registerHook('captchaRequired', self.omegleCaptchaRequired)
		self.omegleClient.registerHook('captchaRejected', self.omegleCaptchaRejected)

		self.thread = Thread(target=self.loop)

	def start(self, isPublic=True):
		self.isPublic = isPublic

		if self.omegleClient.isConnected():
			self.sendToXMPP('Why are you starting me again?')
			return

		self.omegleClient.start()

		self.thread.start()

	def loop(self):
		while self.xmppClient.Process(0.1):
			self.omegleClient.step()

		if self.omegleClient.isConnected():
			self.omegleClient.disconnect()
		self.xmppClient.disconnect()

	def setScope(self, isPublic):
		self.isPublic = isPublic

	def stop(self):
		if self.omegleClient.isConnected():
			self.omegleClient.disconnect()
		self.xmppClient.sendPresence(typ='unavailable')
		self.connected = False

	def kick(self):
		self.sendToOmegle("** You have been kicked out of the groupchat. Better luck next time.")
		self.stop()

	def sendCaptcha(self, captchaText):
		self.omegleClient.confirmCaptcha(unicode(captchaText).encode('utf-8'))

	def sendToOmegle(self, msg):
		print '[o:' + self.nick + '] tx: ' + msg
		self.omegleClient.sendMessage(unicode(msg).encode('utf-8'))

	def sendToXMPP(self, msg):
		self.xmppClient.send(Message(self.muc, unicode(msg), 'groupchat'))

	def xmppMessageHandler(self, client, msg):
		nick = msg.getFrom().getResource()
		if not msg or not msg.getBody() or not nick or nick == self.nick:
			return
		text = msg.getBody().strip()
		if text[:1] == '.' or text[:1] == '!':
			return



		if self.omegleClient.isConnected():
			s = u'<' + nick + u'> ' + unicode(text);
			self.sendToOmegle(s)

	def xmppPresenceHandler(self, client, pres):
		nick = pres.getFrom().getResource()
		if pres.getType() == 'unavailable':
			if nick == self.nick:
				self.kick()

	def omegleJoin(self):
		presence = Presence(to=self.muc + '/' + self.nick)
		presence.setTag('x', namespace=xmpp.NS_MUC).setTagData('password', '')
		presence.getTag('x').addChild('history', {'maxchars': '0', 'maxstanzas': '0'});
		self.xmppClient.send(presence)
		self.connected = True
		print '[o:' + self.nick + '] joined'
#		self.sendToXMPP('Stranger connected...')

	def omegleMessage(self, msg):
		print '[o:' + self.nick + '] rx: ' + msg
		self.sendToXMPP(msg)

	def omegleLeave(self):
		print '[o:' + self.nick + '] left'
		self.stop()

	def omegleCaptchaRequired(self, url):
		if not self.connected:
			presence = Presence(to=self.muc + '/' + self.nick)
			presence.setTag('x', namespace=xmpp.NS_MUC).setTagData('password', '')
			presence.getTag('x').addChild('history', {'maxchars': '0', 'maxstanzas': '0'});
			self.xmppClient.send(presence)
		print '[o:' + self.nick + '] captcha: ' + url
		self.sendToXMPP('.* CAPTCHA: ' + url)

	def omegleCaptchaRejected(self):
		print '[o:' + self.nick + '] captcha rejected'
		self.sendToXMPP('CAPTCHA rejected, disconnecting...')
		self.stop()