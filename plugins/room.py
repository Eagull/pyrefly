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
from libCommand import Command, Help, Access

class Room(Plugin):
	
	def __init__(self):
		Plugin.__init__(self)
	
	def onLoad(self, bot):
		Plugin.onLoad(self, bot)
		self._rooms = self.bot.db.table('rooms')
	
	@Command('room-group')
	@Help('Get or set the group of this room', usage='[<group>]')
	def cmdRoomGroup(self, muc, user, args, say, whisper):
		if len(args) != 1:
			say("Current room group is: %s" % muc.data['group'])
		else:
			muc.data['group'] = args[0]
			if self._rooms is not None:
				self._rooms.update({'muc': muc.getId()}, {'group': args[0]})
			say("Set room group to: %s" % args[0])
			
