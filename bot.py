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

import libXmpp, db
#from handlers import commandHandler, logHandler, fightHandler, swearHandler, replyHandler
#import pyrefight
#import dictionary

# TODO: add SIGINT and exit handlers

class Pyrefly(object):

	def __init__(self, config):
		self.config = config
		self.client = libXmpp.Client(self.config.get('id'))
		self.db = db.Db('pyrefly', self.config.get('account', 'db'), self.config.get('password', 'db'), self.config.get('spreadsheet', 'db'))
		self.plugins = {}
		self.pluginModules = {}
	
	def connect(self):
		self.db.connect()
		result, err = self.client.connect(self.config.get('password'), 'bot' + self.config.hash[:6])
		if not result:
			print "Error connecting: %s" % err
			exit(1)

	def initialize(self):
		mucTable = self.db.table('muc')
		toJoin = mucTable.get({'autojoin': 'y'})
		for mucToJoin in toJoin:
			self.join(mucToJoin['muc'], mucToJoin['nick'], mucToJoin['password'])
	
	def join(self, muc, nick, password=''):
		return self.client.join(muc, nick, password=password)

	def process(self, timeout=0.1):
		self.client.process(timeout=timeout)
		return True

	def onPresence(self, *args, **kwargs):
		for handler in self.handlers:
			handler.onPresence(*args, **kwargs)

	def onMessage(self, *args, **kwargs):
		for handler in self.handlers:
			handler.onMessage(*args, **kwargs)

	def onRoster(self, *args, **kwargs):
		for handler in self.handlers:
			handler.onRoster(*args, **kwargs)

	def registerHandler(self, handler):
		handler.onRegister()
		self.handlers.append(handler)
	
	def unregisterHandler(self, handler):
		handler.onUnregister()
		self.handlers.remove(handler)

	def loadPlugin(self, name):
		name = "plugin.%s"
		if name in self.plugins:
			return False
		self.pluginModules[name] = __import__(name)
		if not self.pluginModules[name]:
			del self.pluginModules[name]
			return False
		clazz = self.pluginModules[name][name]
		self.plugins[name] = clazz()
		self.plugins[name].onLoad(self)
		return True
		
	def unloadPlugin(self, name):
		for pluginName, plugin in self.plugins:
			if name in plugin.getDependencies():
				self.unloadPlugin(pluginName)
		self.plugins[name].onUnload()
		del self.plugins[name]
	
	def reloadPlugin(self, name):
		if name not in self.pluginModules:
			return False
		plugin = self.plugins[name]
		plugin.onUnload()
		reload(self.pluginModules[name])
		clazz = self.pluginModules[name][name]
		self.plugins[name] = clazz()
		self.plugins[name].onLoad(self)
		for pluginName, plugin in self.plugins:
			if name in plugin.getDependencies():
				plugin.setDependency(pluginName, self.plugins[name])
		

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
