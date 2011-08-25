'''
XMPP Bot
Copyright (C) 2011 Eagull.net

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


class Dispatcher(object):

	def __init__(self, initChars = ['!']):
		self.commands = {}
		self.gates = []
		self.initChars = initChars

	def addGate(self, gate):
		self.gates.append(gate)

	def define(self, name, handler, access='all', argc=0):
		cmd = Command(name, handler, access, argc)
		self.commands[name.lower()] = cmd
		return cmd

	def onMucMessage(self, muc, client, message, jid=None):
		# Only respond for messages which begin with command invocation.
		if message[0:1] not in self.initChars:
			return False

		# Determine what command is being invoked, and exit if we don't handle it.
		cmdStr = message.split(" ", 1)[0][1:].lower()
		if cmdStr not in self.commands:
			return False
		cmd = self.commands[cmdStr]

		# Test this invocation against the gates.
		for gate in self.gates:
			if not gate(muc, client, message, cmd, jid=jid):
				return False

		cmd.dispatch(muc, client, message)
		return True


class Command(object):

	def __init__(self, name, handler, access, argc):
		self.name = name
		self.handler = handler
		self.access = access
		self.argc = argc

	def dispatch(self, muc, client, message):
		# Gate on access restriction of this command.
		if not self.accessGate(muc, client):
			return

		args = self.splitArgs(message)
		if len(args) != self.argc:
			return

		# Closure for easy response
		def say(message):
			muc.sendMessage(message)
			self.handler(muc, client, args, respond)

	def accessGate(self, muc, client):
		if self.access == 'member':
			if not client.isMember():
				return False
		return True

	def splitArgs(self, message):
		return message.split(" ", self.argc)[1:]
