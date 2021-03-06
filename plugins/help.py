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
from libCommand import Command, Help

class Help(Plugin):
	
	def __init__(self):
		Plugin.__init__(self)
	
	def onLoad(self, bot):
		Plugin.onLoad(self, bot)
	
	@Command('help', minArgs=1)
	@Help("You can't possibly be THAT helpless.", usage='<command>')
	def cmdHelp(self, muc, user, args, say, whisper):
		command = self._bot.getDispatcher().getCommand(args[0])
		if command is None:
			say("No such command: !%s" % args[0])
			return
	
		auth = ''
		if not command.hasAccess(user):
			auth = ' (not authorized)'
		say(command.getHelp())
		say("Usage: %s%s %s%s" % (command.getTriggerChar(), command.getTrigger(), command.getUsage(), auth))
