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

	def __init__(self, strJid):
		self.jid = xmpp.JID(strJid)
		self.client = xmpp.Client(self.jid.getDomain(), debug=[])
		self.mucs = {}
		self.handlers = []

	def connect(self, password, resource):
		res = self.client.connect()
		if not res:
			return (False, "Error connecting to server: %s" % jid.getDomain())

		res = self.client.auth(self.jid.getNode(), password, resource)
		if not res:
			return (False, "Error authenticating as %s" % self.jid.getNode())

		self.client.RegisterHandler('presence', self.onRoster)
		self.client.RegisterHandler('message', self.onMessage)

		self.client.sendInitPresence()

		return (True, None)

	def process(self, timeout=0.1):
		self.client.Process(timeout)

	def join(self, mucName, nick, password=''):
		lMucName = mucName.lower()
		if lMucName in self.mucs:
			return self.mucs[lMucName]

		muc = Muc(self, mucName, nick)
		self.mucs[lMucName] = muc
		muc.sendPresence(password)

		return muc

	def emitMucJoin(self, muc, user):
		for handler in self.handlers:
			handler.onMucJoin(muc, user)

	def emitMucPart(self, muc, user):
		for handler in self.handlers:
			handler.onMucPart(muc, user)

	def emitMucNickChange(self, muc, user, oldNick):
		for handler in self.handlers:
			handler.onMucNickChange(muc, user, oldNick)

	def onMessage(self, session, message):
		sender = message.getFrom()
		mucName = sender.getStripped()
		lMucName = mucName.lower()
		nick = sender.getResource()
		toprint = "libXmpp: <%s/%s> %s" % (mucName, nick, message.getBody())
		print toprint.encode('utf-8')

		if lMucName not in self.mucs:
			return

		muc = self.mucs[lMucName]

		# Suppress messages send by this bot itself.
		if nick == muc.getNick():
			return

		user = muc.getUser(nick)

		for handler in self.handlers:
			handler.onMucMessage(muc, user, message.getBody(), jid=sender)

	def onRoster(self, session, presence):
		jid = presence.getFrom()
		mucId = jid.getStripped()
		lMucId = mucId.lower()

		if not lMucId in self.mucs:
			return

		self.mucs[lMucId].onRoster(presence)

	def addHandler(self, handler):
		self.handlers.append(handler)

	def removeHandler(self, handler):
		self.handlers.remove(handler)


class Muc(object):

	def __init__(self, client, name, nick):
		self.client = client
		self.name = name
		self.nick = nick

		self.roomId = "%s/%s" % (name, nick)
		self.jid = JID(self.roomId)
		self.mucId = self.jid.getStripped()
		self.roster = {}

	def getId(self):
		return self.mucId

	def getUser(self, nick):
		if nick not in self.roster:
			return None
		return self.roster[nick]

	def getNick(self):
		return self.nick

	def sendPresence(self, password):
		presence = xmpp.Presence(to=self.roomId)
		x = presence.setTag('x', namespace=xmpp.NS_MUC)
		x.setTagData('password', password)
		x.addChild('history', {'maxchars': '0', 'maxstanzas': '0'});
		self.client.client.send(presence)

	def sendMessage(self, body):
		message = xmpp.protocol.Message(to=self.mucId, body=body, typ='groupchat')
		self.client.client.send(message)

	def setRole(self, user, role, reason=None):
		iqMap = {'role': role}
		if reason is not None:
			iqMap['reason'] = reason
		self.client.client.send(user.iq(iqMap))

	def setAffiliation(self, user, affiliation):
		self.client.client.send(user.iq({'affiliation': affiliation}))

	def onRoster(self, presence):
		nick = presence.getFrom().getResource()

		if presence.getType() == 'unavailable':
			if nick not in self.roster:
				return

			user = self.roster[nick]

			# This unpleasantness checks for and handles nickname changes:
			x = presence.getTag(presence, {}, NS_MUC_USER)
			if x is None:
				return
			item = x.getTag('item')
			status = x.getTag('status')

			if status and status.getAttr('code') == '303':
				newNick = item.getAttr('nick')
				if newNick == nick:
					return

				# nick -> newNick
				user.updateNick(newNick)
				del self.roster[nick]
				self.roster[newNick] = user
				if nick == self.nick:
					self.nick = nick
				self.client.emitMucNickChange(self, user, nick)
			else:
				# Seems like this user was deleted.
				self.client.emitMucPart(self, self.roster[nick])
				del self.roster[nick]
		else:
			if nick in self.roster:
				user = self.roster[nick]
				user.updateFromPresence(nick, presence)
			else:
				self.roster[nick] = self.userFromPresence(nick, presence)
				self.client.emitMucJoin(self, self.roster[nick])
			pass

	def userFromPresence(self, nick, presence):
		return User(self, nick).updateFromPresence(nick, presence)


class User(object):

	def __init__(self, muc, nick):
		self.muc = muc
		self.nick = nick

		self.affiliation = ''
		self.status = 'online'
		self.role = ''
		self.jid = ''

	def getNick(self):
		return self.nick

	def getAffiliation(self):
		return self.affiliation

	def getStatus(self):
		return self.status

	def getRole(self):
		return self.role

	def getJid(self):
		return self.jid

	def setNick(self, nick):
		self.nick = nick

	def updateFromPresence(self, nick, presence):
		status = self.statusFromPresence(presence)
		if status:
			self.status = status

  		x = presence.getTag('x', {}, NS_MUC_USER)
  		if not x:
  			return self

  		item = x.getTag('item')
  		if not item:
  			return self

  		self.affiliation = item.getAttr('affiliation')
  		self.role = item.getAttr('role')
  		self.jid = item.getAttr('jid')

		return self

	def statusFromPresence(self, presence):
		statusMsg = 'online'
		show = presence.getTag('show')
		if show:
			statusMsg = show.getData()

		status = presence.getTag('status')
		if status:
			pass

		return statusMsg

	def setRole(self, role):
		self.muc.setRole(self, role, reason=reason)

	def setAffiliation(self, affiliation):
		self.muc.setAffiliation(self, affiliation)

	def isMember(self):
		return self.affiliation in ['member', 'admin', 'owner']

	def isModerator(self):
		return self.role == 'moderator'

	def isAdmin(self):
		return self.affiliation in ['admin', 'owner']

	def isOwner(self):
		return self.affiliation == 'owner'

	def kick(self, reason):
		self.setRole('none', reason=reason)

	def voice(self, reason=None):
		self.setRole('participant', reason=reason)

	def devoice(self, reason=None):
		self.setRole('visitor', reason=reason)

	def iq(self, attributes):
		iq = xmpp.protocol.Iq('set', NS_MUC_ADMIN, {}, self.mucId)
		item = iq.getTag('query').setTag('item')
		item.setAttr('nick', self.nick)
		for k, v in attributes.items():
			item.setAttr(k, v)
		return iq
