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
		self.overflowHandlers = []
		self.initChars = initChars
	
	def addGate(self, gate):
		self.gates.append(gate)

	def define(self, command):
		trigger = command.getTrigger().lower()
		if trigger in self.commands:
			return False
		self.commands[trigger] = command
		return True
	
	def undefine(self, command):
		trigger = command.getTrigger().lower()
		if trigger not in self.commands:
			return
		del self.commands[trigger]
	
	def onMucMessage(self, muc, client, message, jid=None):
		# Only respond for messages which begin with command invocation.
		if message[0:1] not in self.initChars:
			return False
		
		# Determine what command is being invoked, and exit if we don't handle it.
		cmdStr = message.split(" ", 1)[0][1:].lower()
		if cmdStr not in self.commands:
			self.sendOverflow(muc, client, cmdStr, message, jid)
		cmd = self.commands[cmdStr]
		
		# Test this invocation against the gates.
		for gate in self.gates:
			if not gate(muc, client, message, cmd, jid=jid):
				# Don't treat this as an overflow.
				return False
		
		cmd.dispatch(muc, client, message)
		return True
	
	def newCommand(self, trigger):
		return CommandBuilder(self, trigger)
	

class Command(object):
	
	def __init__(self, trigger, minArgs=0, maxArgs = None):
		self.trigger = trigger
		self.minArgs = minArgs
		self.maxArgs = maxArgs
	
	def __call__(self, func):
		func._command = {}
		func._command['trigger'] = self.trigger.lower()
		func._command['minArgs'] = self.minArgs
		if self.maxArgs is not None:
			func._command['maxArgs'] = self.maxArgs
		return func


class Help(object):

	def __init__(self, helpStr):
		self.helpStr = helpStr
	
	def __call__(self, func):
		if not hasattr('_command', func):
			return func
		
		func._command['help'] = self.helpStr
		return func


class Access(object):
	
	def __init__(self, access):
		self.access = access
	
	def __call__(self, func):
		if not hasattr('_command', func):
			return func
		
		func._command['access'] = access
		return func