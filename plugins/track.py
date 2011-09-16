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

from plugin import Plugin
import re

class Track(Plugin):

	def __init__(self):
		Plugin.__init__(self)

	def onLoad(self, bot):
		Plugin.onLoad(self, bot)
		self._users = bot.getDb().table('users')
		self._userData = {}
		for row in self._users.getAll():
			self._userData[row['mask']] = row
		self._loadUsers()

	def onUnload(self):
		Plugin.onUnload(self)
	
	def onRoomJoin(self, room, user):
		self._trackUser(room, user)

	def _loadUsers(self):
		for room in self._bot.getClient().getRooms():
			for user in room.getMembers():
				self._trackUser(room, user)

	def _trackUser(self, room, user):
		userId = user.getId()
		if userId not in self._userData and room.getNick() != user.getNick():
			self._userData[userId] = {'mask': userId, 'password': '', 'seen_ts': '0'}
			self._users.put(self._userData[userId])
			
