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

from plugin import Plugin, Authorizer
from libCommand import Command, Help
import re

class RoleAuthorization(Plugin):

	def __init__(self):
		Plugin.__init__(self)

	def onLoad(self, bot):
		Plugin.onLoad(self, bot)
		self._table = bot.getDb().table('roleMembers')
		self._refresh()
	
	def _refresh(self):
		self._roles = dict()
		entries = self._table.getAll()
		for entry in entries:
			self._addEntry(entry)
	
	def _addEntry(self, entry):
		role = entry['role']
		if role not in self._roles:
			self._roles[role] = {'global': [], 'groups': {}, 'rooms': {}}

		identity = entry['identity']
		group = entry['group']
		room = entry['room']
		if group:
			sub = self._roles[role]['groups']
			if group not in sub:
				sub[group] = []
			sub[group].append(identity)
		elif room:
			sub = self._roles[role]['rooms']
			if room not in sub:
				sub[room] = []
			sub[room].append(identity)
		else:
			self._roles[role]['global'].append(identity)
	
	def onUnload(self):
		Plugin.onUnload(self)
	
	def _isAuthorizedGlobally(self, role, identity):
		if role not in self._roles:
			return False
		return identity in self._roles[role]['global']

	def _isAuthorizedByGroup(self, group, role, identity):
		if role not in self._roles:
			return False
		if group not in self._roles[role]['groups'][group]:
			return False
		return identity in self._roles[role]['groups'][group]
	
	def _isAuthorizedByRoom(self, room, role, identity):
		if role not in self._roles:
			return False
		if room not in self._roles[role]['rooms']:
			return False
		return identity in self._roles[role]['rooms'][room]

	@Authorizer('role')
	def authorize(self, room, user, role):
		identity = user.getIdentity()
		if not identity:
			print "No identity"
			return False

		group = room.data['group']
		print "Checking user %s for room %s in group %s" % (identity, room.getName(), group)

		return (self._isAuthorizedGlobally(role, identity)
				or self._isAuthorizedByGroup(group, role, identity)
				or self._isAuthorizedByRoom(room.getName(), role, identity))

	@Command('role-auth-check', minArgs=1, maxArgs=1)
	@Help('Check your role-based auth status', usage='<role>')
	def cmdAuthCheck(self, room, user, args, say, whisper):
		role = args[0]
		if user.isInRole(room, 'role', role):
			say("You are authorized for role: xmpp:%s" % role)
		else:
			say("You are not authorized for role: xmpp:%s" % role)


	@Command('role-auth-refresh', maxArgs=0)
	@Help('Refresh the role database')
	def cmdRefresh(self, room, user, args, say, whisper):
		self._refresh()

		say("Refresh complete, %d roles defined" % len(self._roles.keys()))
