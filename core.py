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

class CoreHandler(Handler):
	
	def __init__(self, bot):
		Handler.__init__(self)
		self.bot = bot
	
	def onMessage(self, client, message):
		if not message[0] == '!':
			return
		args = message.split(' ')
		if args[0] == '!load' and args.length == 2:
			bot.loadPlugin(args[1])
		elif args[0] == '!unload' and args.length == 2:
			bot.unloadPlugin(args[2])
		elif args[0] == '!reload' and args.length == 2:
			bot.reloadPlugin(args[3])