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
import types

class Plugin(Handler):
	
	def __init__(self):
		Handler.__init__(self)
		self.bot = None

	def getDependencies(self):
		return tuple()
	
	def setDependency(self, name, dep):
		pass

	def onLoad(self, bot):
		self.bot = bot
		self.bot.registerHandler(self)
		self._registerCommands()

	def onUnload(self):
		self.bot.unregisterHandler(self)

	def _registerCommands(self):
		for key in dir(self):
			func = getattr(key, self)
			if isinstance(func, types.FunctionType) and hasattr('_command', func):
				self.bot.dispatcher.registerCommandHandler(func)