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

#import xmpp
import config

from db import Db
from core import Core
from libXmpp import Client
from handler import Handler
import sys, os
#from handlers import commandHandler, logHandler, fightHandler, swearHandler, replyHandler
#import pyrefight
#import dictionary

# TODO: add SIGINT and exit handlers

class Pyrefly(Handler):

	def __init__(self, config):
		self.config = config
		self.client = Client(self.config.get('id'))
		self.client.addHandler(self)
		self.db = Db('pyrefly', self.config.get('account', 'db'), self.config.get('password', 'db'), self.config.get('spreadsheet', 'db'))
		self.plugins = {}
		self.pluginModules = {}
		self.handlers = [Core(self)]

		# Set up the import path for plugins
		myPath = os.path.abspath(__file__)
		pluginPath = os.path.join(myPath.rsplit(os.sep, 1)[0], "plugins")
		print "Path for plugins is: %s" % pluginPath
		sys.path.append(pluginPath)

	def connect(self):
		self.db.connect()
		result, err = self.client.connect(self.config.get('password'), 'bot' + self.config.hash[:6])
		if not result:
			print "Error connecting: %s" % err
			exit(1)

	def initialize(self):
		toJoin = []
		for mucId in self.config.getRoomList():
			toJoin.append({'muc': mucId, 'nick': self.config.get('nick', mucId), 'password': ''})

		for mucToJoin in toJoin:
			muc = self.join(mucToJoin['muc'], mucToJoin['nick'], password=mucToJoin['password'])
			if muc is not None:
				muc.data = mucToJoin


	def join(self, muc, nick, password=''):
		return self.client.join(muc, nick, password=password)

	def process(self, timeout=0.1):
		self.client.process(timeout=timeout)
		return True

	def onMucMessage(self, *args, **kwargs):
		for handler in self.handlers:
			handler.onMucMessage(*args, **kwargs)

	def registerHandler(self, handler):
		self.handlers.append(handler)

	def unregisterHandler(self, handler):
		self.handlers.remove(handler)

	def loadPlugin(self, name):
		if name in self.plugins:
			return (False, "Plugin %s is already loaded" % name)
		source = None
		if name in self.pluginModules:
			source = "reloaded"
			reload(self.pluginModules[name])
		else:
			importName = name.lower()
			source = "imported"
			try:
				self.pluginModules[name] = __import__(importName, globals(), locals(), [], 0)
			except ImportError:
				return (False, "No such module: %s" % importName)

		if not self.pluginModules[name]:
			print "import failed!"
			del self.pluginModules[name]
			return (False, "Module not defined after import")
		print "Imported: %s" % self.pluginModules[name]

		try:
			clazz = getattr(self.pluginModules[name], name)
		except AttributeError:
			return (False, "Module has no class defined")

		print "Class: %s" % clazz
		if not clazz:
			return (False, "Class not defined after import")
		self.plugins[name] = clazz()
		self.plugins[name].onLoad(self)
		return (True, source)

	def unloadPlugin(self, name):
		if name not in self.plugins:
			return (False, None, "not loaded")

		toUnload = []
		unloaded = []
		for pluginName, plugin in self.plugins.items():
			if name in plugin.getDependencies():
				toUnload.append(pluginName)

		for pluginName in toUnload:
			result, extraUnloaded, err = self.unloadPlugin(pluginName)
			for unloadedName in extraUnloaded:
				unloaded.append(unloadedName)
			if not result:
				return (False, unloaded, err)
			unloaded.append(pluginName)

		self.plugins[name].onUnload()
		del self.plugins[name]
		return (True, unloaded, None)

	def reloadPlugin(self, name):
		if name not in self.plugins:
			return (False, "Not loaded")
		plugin = self.plugins[name]
		plugin.onUnload()
		reload(self.pluginModules[name])
		try:
			clazz = getattr(self.pluginModules[name], name)
		except AttributeError:
			return (False, "Class no longer defined")
		self.plugins[name] = clazz()
		self.plugins[name].onLoad(self)
		for pluginName, plugin in self.plugins.items():
			if name in plugin.getDependencies():
				plugin.setDependency(pluginName, self.plugins[name])
		return (True, None)


##~ client.RegisterHandler('message', logHandler.messageHandler)
#client.RegisterHandler('presence', logHandler.presenceHandler)
#client.RegisterHandler('presence', xmppUtils.rosterHandler)
#client.RegisterHandler('message', commandHandler.messageHandler)

#client.RegisterHandler('message', replyHandler.messageHandler)
#client.RegisterHandler('message', swearHandler.messageHandler)

#client.RegisterHandler('message', fightHandler.messageHandler)
#client.RegisterHandler('presence', pyrefight.presHandler)

if __name__ == '__main__':
	pyrefly = Pyrefly(config)
	pyrefly.connect()
	pyrefly.initialize()
	try:
		while pyrefly.process():
			pass
	except KeyboardInterrupt:
		exit(0)
