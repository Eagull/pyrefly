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
from libXmpp import XmppClient
from handler import Handler, EventBroadcaster
from libCommand import Dispatcher

import sys, os

class Pyrefly(Handler):

	def __init__(self, config):
		self._config = config
		self._client = XmppClient(self._config.get('id'))
		self._db = Db('pyrefly', self._config.get('account', 'db'), self._config.get('password', 'db'), self._config.get('spreadsheet', 'db'))
		self._plugins = {}
		self._pluginModules = {}
		self._dispatcher = Dispatcher()
		self._broadcaster = EventBroadcaster()
		self._broadcaster.addHandler(Core(self))
		self._client.addHandler(self._broadcaster)
		# Set up the import path for plugins
		myPath = os.path.abspath(__file__)
		pluginPath = os.path.join(myPath.rsplit(os.sep, 1)[0], "plugins")
		print "Path for plugins is: %s" % pluginPath
		sys.path.append(pluginPath)

	def connect(self):
		self._db.connect()
		result, err = self._client.connect(self._config.get('password'), 'bot' + self._config.hash[:6])
		if not result:
			print "Error connecting: %s" % err
			exit(1)
		print "Connected!"

	def initialize(self):
		joinMap = {}
		table = self.db.table('rooms')
		if table is not None:
			rows = table.get({'autojoin': 'y'})
			for row in rows:
				joinMap[row['muc']] = row
		for mucId in self.config.getRoomList():
			if mucId not in joinMap:
				group = self.config.get('group', mucId)
				if not group:
					group = 'global'
				nick = self.config.get('nick', mucId)
				name = mucId.split('@')[0]
				data = {'name': name, 'muc': mucId, 'nick': nick, 'password': '', 'group': group, 'autojoin': 'y', 'control': 'n'}
				joinMap[mucId] = data
				if table is not None:
					table.put(data)

		for mucToJoin in joinMap.values():
			muc = self.join(mucToJoin['muc'], mucToJoin['nick'], password=mucToJoin['password'])
			if muc is not None:
				muc.data = mucToJoin

	def join(self, muc, nick, password=''):
		return self._client.join(muc, nick, password=password)

	def process(self, timeout=0.1):
		self._client.process(timeout=timeout)
		return True

	def registerHandler(self, handler):
		self._broadcaster.addHandler(handler)

	def unregisterHandler(self, handler):
		self._broadcaster.removeHandler(handler)

	def loadPlugin(self, name):
		if name in self._plugins:
			return (False, "Plugin %s is already loaded" % name)
		source = None
		if name in self._pluginModules:
			source = "reloaded"
			reload(self._pluginModules[name])
		else:
			importName = name.lower()
			source = "imported"
			try:
				self._pluginModules[name] = __import__(importName, globals(), locals(), [], 0)
			except ImportError:
				return (False, "No such module: %s" % importName)

		if not self._pluginModules[name]:
			del self._pluginModules[name]
			return (False, "Module not defined after import")

		try:
			clazz = getattr(self._pluginModules[name], name)
		except AttributeError:
			return (False, "Module has no class defined")

		if not clazz:
			return (False, "Class not defined after import")
		self._plugins[name] = clazz()
		self._plugins[name].onLoad(self)
		return (True, source)

	def unloadPlugin(self, name):
		if name not in self._plugins:
			return (False, None, "not loaded")

		toUnload = []
		unloaded = []
		for pluginName, plugin in self._plugins.items():
			if name in plugin.getDependencies():
				toUnload.append(pluginName)

		for pluginName in toUnload:
			result, extraUnloaded, err = self.unloadPlugin(pluginName)
			for unloadedName in extraUnloaded:
				unloaded.append(unloadedName)
			if not result:
				return (False, unloaded, err)
			unloaded.append(pluginName)

		self._plugins[name].onUnload()
		del self._plugins[name]
		return (True, unloaded, None)

	def reloadPlugin(self, name):
		if name not in self._plugins:
			return (False, "Not loaded")
		plugin = self._plugins[name]
		plugin.onUnload()
		reload(self._pluginModules[name])
		try:
			clazz = getattr(self._pluginModules[name], name)
		except AttributeError:
			return (False, "Class no longer defined")
		self._plugins[name] = clazz()
		self._plugins[name].onLoad(self)
		for pluginName, plugin in self._plugins.items():
			if name in plugin.getDependencies():
				plugin.setDependency(pluginName, self._plugins[name])
		return (True, None)


if __name__ == '__main__':
	pyrefly = Pyrefly(config)
	pyrefly.connect()
	pyrefly.initialize()
	try:
		while pyrefly.process():
			pass
	except KeyboardInterrupt:
		exit(0)
