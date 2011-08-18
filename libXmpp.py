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
	
	def onRoster(self, session, presence):
		jid = presence.getFrom()
		mucId = jid.getStripped()
		lMucId = mucId.lower()
		
		if not lMucId in self.mucs:
			return
		
		self.mucs[lMucId].onRoster(presence)
		
		
class Muc(object):

	def __init__(self, client, name, nick):
		self.client = client
		self.name = name
		self.nick = nick
		
		self.roomId = "%s/%s" % (name, nick)
		self.jid = JID(self.roomId)
		self.mucId = self.jid.getStripped()
		self.roster = {}
	
	def sendPresence(self, password):
		presence = xmpp.Presence(to=self.roomId)
		x = presence.setTag('x', namespace=xmpp.NS_MUC)
		x.setTagData('password', password)
		x.addChild('history', {'maxchars': '0', 'maxstanzas': '0'});

		self.client.client.sendPresence(presence)
	
	def sendMessage(self, body):
		message = xmpp.protocol.Message(to=self.mucId, body=body, type='groupchat')
		self.client.client.send(message)
	
	def onRoster(self, presence):
		nick = presence.getFrom().getResource()
		
		if presence.getType() == 'unavailable':
			if nick not in self.roster:
				return
			
			# Either they are changing nicks, or leaving.
			x = presence.getTag(x, {}, NS_MUC_USER)
			item = x.getTag('item')
			status = x.getTag('status')
			
			if status and status.getAttr('code') == '303':
				newNick = item.getAttr('nick')
				if newNick == nick:
					return
				
				user = self.roster[nick]
				user.updateNick(newNick)
				del self.roster[nick]
				self.roster[newNick] = user
			else:
				# Seems like this user was deleted.
				del self.roster[nick]
		else:
			if nick in self.roster:
				
			self.roster[nick] = self.userFromPresence(nick, presence)
			pass
		
	def userFromPresence(self, nick, presence):
		status = self.statusFromPresence(presence)
	
class User(object):
	
	def __init__(self, muc, nick):
		self.muc = muc
		self.nick = nick
		self.jid = JID("%s/%s" % (muc, nick))
		
		self.affiliation = ''
		self.status = 'online'
		self.role = role
		
	def updateFromPresence(self, presence):
		status = self.statusFromPresence(presence)
		if status:
			self.status = status
		
		
		
	def statusFromPresence(self, presence):
		statusMsg = 'online'
		show = presence.getTag('show')
		if show:
			statusMsg = show.getData()
		
		status = pres.getTag('status')
		if status:
			pass
			
		return statusMsg
			