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
from libChat import Member
import types


class Authorizer(object):

	def __init__(self, category):
		self._category = category
	
	def __call__(self, fn):
		cat = self._category
		def replace(caller, room, user, category, role):
			if category != cat:
				return False
			return fn(caller, room, user, role)
		replace._authorizer = True
		return replace


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
		self._registerInternals()

	def onUnload(self):
		self.bot.unregisterHandler(self)
		self._unregisterInternals()

	def _registerInternals(self):
		for key in dir(self):
			func = getattr(self, key)
			if hasattr(func, '_command') and 'trigger' in func._command:
				self.bot.getDispatcher().registerCommandHandler(func)
			elif hasattr(func, '_authorizer'):
				Member.addRoleHandler(func)
	
	def _unregisterInternals(self):
		for key in dir(self):
			func = getattr(self, key)
			if hasattr(func, '_command') and 'trigger' in func._command:
				self.bot.getDispatcher().unregisterCommandHandler(func)
			elif hasattr(func, '_authorizer'):
				Member.removeRoleHandler(func)
