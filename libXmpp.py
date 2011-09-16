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
from libChat import Client, Room, Member
import xmpp


class XmppClient(Client):

	def __init__(self, strJid):
		Client.__init__(self)
		self._jid = xmpp.JID(strJid)
		self._client = xmpp.Client(self._jid.getDomain(), debug=[])

	def getClient(self):
		return self._client

	def connect(self, password, resource):
		res = self._client.connect()
		if not res:
			return (False, "Error connecting to server: %s" % jid.getDomain())

		res = self._client.auth(self._jid.getNode(), password, resource)
		if not res:
			return (False, "Error authenticating as %s" % self._jid.getNode())

		self._client.RegisterHandler('presence', self.onRoster)
		self._client.RegisterHandler('message', self.onMessage)

		self._client.sendInitPresence()

		return (True, None)

	def process(self, timeout=0.1):
		self._client.Process(timeout)

	def join(self, mucName, nick, password=''):
		muc = self.getRoom(mucName)
		if muc is not None:
			return muc

		muc = XmppMuc(self, mucName, nick)
		muc.sendPresence(password)
		self._addRoom(muc)

		return muc

	def onMessage(self, session, message):
		sender = message.getFrom()
		mucName = sender.getStripped()
		lMucName = mucName.lower()
		nick = sender.getResource()
		toprint = "libXmpp: <%s/%s> %s" % (mucName, nick, message.getBody())
		print toprint.encode('utf-8')
		
		muc = self.getRoom(mucName)
		if not muc:
			return

		# Suppress messages send by this bot itself.
		if nick == muc.getNick():
			return

		user = muc.getMemberByNick(nick)

		if message.getBody() is None:
			return

		self.onRoomMessage(muc, user, message.getBody(), jid=sender)

	def onRoster(self, session, presence):
		jid = presence.getFrom()
		mucId = jid.getStripped()
		lMucId = mucId.lower()

		muc = self.getRoom(mucId)
		if not muc:
			return

		muc.onRoster(presence)


class XmppMuc(Room):

	def __init__(self, client, name, nick):
		Room.__init__(self, client, name)
		self._nick = nick

		self._roomId = "%s/%s" % (name, nick)
		self._jid = JID(self._roomId)

	def getNick(self):
		return self._nick

	def sendPresence(self, password):
		presence = xmpp.Presence(to=self._roomId)
		x = presence.setTag('x', namespace=xmpp.NS_MUC)
		x.setTagData('password', password)
		x.addChild('history', {'maxchars': '0', 'maxstanzas': '0'});
		self.getClient().getClient().send(presence)

	def sendMessage(self, body):
		message = xmpp.protocol.Message(to=self.getName(), body=body, typ='groupchat')
		self.getClient().getClient().send(message)

	def setRole(self, user, role, reason=None):
		iqMap = {'role': role}
		if reason is not None:
			iqMap['reason'] = reason
		self.getClient().getClient().send(user.iq(iqMap))

	def setAffiliation(self, user, affiliation):
		self.getClient().getClient().send(user.iq({'affiliation': affiliation}))

	def onRoster(self, presence):
		nick = presence.getFrom().getResource()

		if presence.getType() == 'unavailable':

			user = self.getMemberByNick(nick)
			if user is None:
				return

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

				# nick -> newNick. This is hacky.
				self.removeMember(user)
				user.updateNick(newNick)
				self.addMember(user)
				if nick == self._nick:
					self._nick = nick
				self.getClient().onRoomNickChange(self, user, nick)
			else:
				user = self.getMemberByNick(nick)
				if user is not None:
					self.getClient().onRoomPart(self, user)
				self.removeMember(nick)
		else:
			user = self.getMemberByNick(nick)
			if user is None:
				user = self.userFromPresence(nick, presence)
				self.addMember(user)
				self.getClient().onRoomJoin(self, user)
			else:
				user.updateFromPresence(nick, presence)

	def userFromPresence(self, nick, presence):
		return XmppMucMember(self, nick).updateFromPresence(nick, presence)


class XmppMucMember(Member):

	def __init__(self, room, nick):
		Member.__init__(self, room, nick)
		self._affiliation = ''
		self._status = 'online'
		self._role = ''
		self._identity = None

	def sendMessage(self, body):
		message = xmpp.protocol.Message(to=self._jid, body=body)
		self.getRoom().getClient().getClient().send(message)
	
	def getNick(self):
		return self._nick
	
	def getId(self):
		return self._jid

	def getAffiliation(self):
		return self._affiliation

	def getStatus(self):
		return self._status

	def getRole(self):
		return self._role

	def getJid(self):
		return self._jid
	
	def getIdentity(self):
		if self._identity is not None:
			return self._identity
		if self._jid is not None:
			return self._jid.split('/', 1)[0]
		return "%s/%s" % (self.getRoom().getName(), self.getNick())

	def setNick(self, nick):
		self._nick = nick

	def updateFromPresence(self, nick, presence):
		status = self._statusFromPresence(presence)
		if status:
			self._status = status

  		x = presence.getTag('x', {}, NS_MUC_USER)
  		if not x:
  			return self

  		item = x.getTag('item')
  		if not item:
  			return self

  		self._affiliation = item.getAttr('affiliation')
  		self._role = item.getAttr('role')
  		self._jid = item.getAttr('jid')

		return self

	def _statusFromPresence(self, presence):
		statusMsg = 'online'
		show = presence.getTag('show')
		if show:
			statusMsg = show.getData()

		status = presence.getTag('status')
		if status:
			pass

		return statusMsg

	def setRole(self, role):
		self.getRoom().setRole(self, role, reason=reason)

	def setAffiliation(self, affiliation):
		self.getRoom().setAffiliation(self, affiliation)

	def isMember(self):
		return self._affiliation in ['member', 'admin', 'owner']

	def isModerator(self):
		return self._role == 'moderator'

	def isAdmin(self):
		return self._affiliation in ['admin', 'owner']

	def isOwner(self):
		return self._affiliation == 'owner'

	def kick(self, reason):
		self.setRole('none', reason=reason)

	def voice(self, reason=None):
		self.setRole('participant', reason=reason)

	def devoice(self, reason=None):
		self.setRole('visitor', reason=reason)

	def iq(self, attributes):
		iq = xmpp.protocol.Iq('set', NS_MUC_ADMIN, {}, self.getRoom().getName())
		item = iq.getTag('query').setTag('item')
		item.setAttr('nick', self._nick)
		for k, v in attributes.items():
			item.setAttr(k, v)
		return iq
