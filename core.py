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

class Core(Handler):

	def __init__(self, bot):
		Handler.__init__(self)
		self.bot = bot

	def onMucMessage(self, muc, client, message, jid=None):
		if client is None:
			return

		if not message:
			return

		#~ uncomment if debugging
		#~ toprint = "Core.onMucMessage: %s/%s - %s" % (muc.getId(), client.getNick(), message)
		#~ print toprint.encode('utf-8')
		if not message[0] == '!':
			return
		args = message.split(' ')
		length = len(args)
		if args[0] == '!load' and length == 2:
			result, err = self.bot.loadPlugin(args[1])
			if not result:
				muc.sendMessage("Import failed: %s" % err)
			else:
				muc.sendMessage("Plugin %s loaded (%s)" % (args[1], err))
		elif args[0] == '!unload' and length == 2:
			result, otherUnloaded, err = self.bot.unloadPlugin(args[1])
			if otherUnloaded is not None:
				for plugin in otherUnloaded:
					muc.sendMessage("Plugin %s unloaded as dependency of %s" % (plugin, args[1]))
			if not result:
				muc.sendMessage("Error unloading %s: %s" % (args[1], err))
			else:
				muc.sendMessage("Plugin %s unloaded" % args[1])

		elif args[0] == '!reload' and length == 2:
			result, err = self.bot.reloadPlugin(args[1])
			if not result:
				muc.sendMessage("Error reloading %s: %s" % (args[1], err))
			else:
				muc.sendMessage("Plugin %s reloaded" % args[1])
