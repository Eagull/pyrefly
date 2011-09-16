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

from handler import Handler

class Dispatcher(Handler):
	def __init__(self, initChars = ['!']):
		Handler.__init__(self)
		self.commands = {}
		self.overflowHandlers = []
		self.initChars = initChars

	def getCommand(self, trigger):
		trigger = trigger.lower()
		if trigger not in self.commands:
			return None
		return self.commands[trigger]
		
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
	
	def onRoomMessage(self, room, client, message, jid=None):
		# Only respond for messages which begin with command invocation.
		if message[0:1] not in self.initChars:
			return False

		# Determine what command is being invoked, and exit if we don't handle it.
		cmdStr = message.split(" ", 1)[0][1:].lower()
		if cmdStr not in self.commands:
		  return
		cmd = self.commands[cmdStr]

		cmd(room, client, message, jid=jid)
		return True
	
	def registerCommandHandler(self, func):
		commandInfo = func._command
		command = CommandHandle(self, func, commandInfo)
		trigger = command.getTrigger()
		if trigger in self.commands:
			return False
		
		self.commands[trigger] = command
		return command
	
	def unregisterCommandHandler(self, func):
		trigger = func._command['trigger']
		if trigger in self.commands:
		  del self.commands[trigger]
	
	def getTriggerChar(self):
		return self.initChars[0]
		

class CommandHandle(object):
	
	def __init__(self, dispatcher, handler, params):
		self.dispatcher = dispatcher
		self.handler = handler
		self.trigger = params['trigger']
		self.minArgs = params['minArgs']
		
		self.maxArgs = None
		if 'maxArgs' in params:
			self.maxArgs = params['maxArgs']
		
		self.access = None
		if 'access' in params:
			self.access = params['access']
		
		self.helpStr = None
		if 'help' in params:
			self.helpStr = params['help']
		
		self.usage = ''
		if 'usage' in params:
			self.usage = params['usage']
	
	def getTrigger(self):
		return self.trigger
	
	def getHelp(self):
	  return self.helpStr
	
	def getUsage(self):
		return self.usage
	
	def getTriggerChar(self):
		return self.dispatcher.getTriggerChar()
		
	def showHelp(self, room):
		if self.helpStr is not None:
			room.sendMessage(self.helpStr)
		self.showUsage(room)
	
	def showUsage(self, room):
		if self.usage != '':
			room.sendMessage('Usage: %s%s %s' % (self.dispatcher.initChars[0], self.trigger, self.usage))
	
	def hasAccess(self, user):
		if self.access is None:
			return True
		category, role = self.access
		return user.isInRole(category, role)
	
	def parseArgs(self, message):
		if self.maxArgs is not None:
			return message.split(" ", self.maxArgs)[1:]
		else:
			return message.split(" ")[1:]

	def __call__(self, room, user, message, jid=None):
		if not self.hasAccess(user):
			return False
			
		args = self.parseArgs(message.strip())
		
		say = lambda reply: room.sendMessage(reply)
		whisper = lambda reply: user.sendMessage(reply)
		
		if len(args) < self.minArgs:
			self.showUsage(user)
			return
		
		self.handler(room, user, args, say, whisper)
		

class Command(object):
	
	def __init__(self, trigger, minArgs=0, maxArgs=None):
		self.trigger = trigger
		self.minArgs = minArgs
		self.maxArgs = maxArgs
	
	def __call__(self, func):
		if not hasattr(func, '_command'):
			func._command = {}
		func._command['trigger'] = self.trigger.lower()
		func._command['minArgs'] = self.minArgs
		if self.maxArgs is not None:
			func._command['maxArgs'] = self.maxArgs
		return func


class Help(object):

	def __init__(self, helpStr, usage=''):
		self.helpStr = helpStr
		self.usage = usage
	
	def __call__(self, func):
		if not hasattr(func, '_command'):
			func._command = {}
		
		func._command['help'] = self.helpStr
		func._command['usage'] = self.usage
		return func


class Access(object):
	
	def __init__(self, category, role):
		self._category = category
		self._role = role
	
	def __call__(self, func):
		if not hasattr(func, '_command'):
			func._command = {}
		
		func._command['access'] = (self._category, self._role)
		return func
