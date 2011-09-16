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

from libCommand import Command, Help

class Broken(Plugin):

	def __init__(self):
		Plugin.__init__(self)

	def onLoad(self, bot):
		Plugin.onLoad(self, bot)

	def onUnload(self):
		Plugin.onUnload(self)

	@Command('crash', maxArgs=0)
	@Help('Attempt to crash the bot with an AttributeError in the command handler.')
	def cmdCrash(self, room, user, args, say, whisper):
		say("Brace yourselves!")
		say(self._nonexist)
	
	def onRoomMessage(self, room, user, message, jid=None):
		self._break = self._nonexist
