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
import re
from random import shuffle

KICK_MESSAGES = [
	'What? They had it coming.',
	'Hasta la vista, baby.',
	'Wow, not gonna miss that one.',
	'/me feels like a jerk now.',
	'This is turning me on.',
	'Okay, who\'s next?',
	'Was that really necessary?',
	'Does that make you feel good?',
	'That never gets old!'
]

def RandomKickMessage():
	shuffle(KICK_MESSAGES)
	return KICK_MESSAGES[0]

class RoomAdmin(Plugin):

	def __init__(self):
		Plugin.__init__(self)

	def onLoad(self, bot):
		Plugin.onLoad(self, bot)

	def onUnload(self):
		Plugin.onUnload(self)
	
	def _multiCmd(self, room, user, args, say, op):
		missing = list()
		for nick in args:
			if not nick:
				continue

			member = room.getMember(nick)
			if not member:
				missing.append(nick)
				continue

			op(member)

		if len(missing) > 0:
			say("Not found: %s" % ", ".join(missing))


	@Command('voice', minArgs=1)
	@Access('xmpp', 'moderator')
	@Help('Voice members in the room', usage='<nick> [<nick> ... <nick>]')
	def cmdMultiVoice(self, room, user, args, say, whisper):
		self._multiCmd(room, user, args, say, lambda member: member.voice())
	
	@Command('devoice', minArgs=1)
	@Access('xmpp', 'moderator')
	@Help('Devoice members in the room', usage='<nick> [<nick> ... <nick>]')
	def cmdMultiDevoice(self, room, user, args, say, whisper):
		self._multiCmd(room, user, args, say, lambda member: member.devoice())

	@Command('kick', minArgs=1, maxArgs=2)
	@Access('xmpp', 'moderator')
	@Help('Kick someone from the room', usage='<nick> [<reason>]')
	def cmdKick(self, room, user, args, say, whisper):
		member = room.getMember(args[0])
		if member is None:
			say("Not found: %s" % args[0])
			return
		if member.isModerator() and not user.isAdmin():
			say("That's not very nice.")
			return
		reason = "Requested by %s" % user.getNick()
		if len(args) > 1:
			reason = args[1]
		member.kick(reason)
		say(RandomKickMessage())
