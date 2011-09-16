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

from plugin import Plugin
from libCommand import Command, Help, Access
import time

class Dictionary(Plugin):

	def __init__(self):
		Plugin.__init__(self)
		
	def onLoad(self, bot):
		Plugin.onLoad(self, bot)
		self._dict = self.bot.getDb().table('dictionary')
	
	@Command('learn', minArgs=2, maxArgs=2)
	@Access('xmpp', 'member')
	@Help('Learn a new dictionary definition', usage='<term> <definition>')
	def cmdLearn(self, muc, client, args, say, whisper):
		term, defin = (args[0], args[1])
		term = term.lower()

		if len(defin) > 3 and defin[0:3] == '=> ':
			defin = defin[3:].trim()

		current, scope = self._getDefinition(term, muc)
	
		if current is not None and scope != 'global':
			defScope = ''
			if scope == 'private':
				defScope = 'privately'
			say("%s is already defined%s by %s: %s" % (term, current['author'], current['def']))
			return

		self._dict.put({'term': term, 'group': muc.data['group'], 'author': client.getNick(), 'def': defin, 'ts': int(time.time())})
		say("Defined %s" % term)

	@Command('learn-global', minArgs=2, maxArgs=2)
	@Access('xmpp', 'member')
	@Help('Learn a new global dictionary definition', usage='<term> <definition>')
	def cmdLearnGlobal(self, muc, client, args, say, whisper):
		term, defin = (args[0], args[1])
		term = term.lower()

		if len(defin) > 3 and defin[0:3] == '=> ':
			defin = defin[3:].trim()

		current = self._dict.getOne({'term': term, 'room': '', 'group': ''})
	
		if current is not None:
			say("%s is already defined globally by %s: %s" % (term, current['author'], current['def']))
			return

		self._dict.put({'term': term, 'muc': '', 'group': '', 'author': client.getNick(), 'def': defin, 'ts': int(time.time())})
		say("Defined %s globally" % term)

	@Command('learn-private', minArgs=2, maxArgs=2)
	@Access('xmpp', 'member')
	@Help('Learn a new private dictionary definition', usage='<term> <definition>')
	def cmdLearnPrivate(self, muc, client, args, say, whisper):
		term, defin = (args[0], args[1])
		term = term.lower()

		if len(defin) > 3 and defin[0:3] == '=> ':
			defin = defin[3:].trim()

		current = self._dict.getOne({'term': term, 'room': muc.getId()})
	
		if current is not None:
			say("%s is already defined privately by %s: %s" % (term, current['author'], current['def']))
			return

		self._dict.put({'term': term, 'room': muc.getId(), 'author': client.getNick(), 'def': defin, 'ts': int(time.time())})
		say("Defined %s" % term)
	
	@Command('forget', minArgs=1)
	@Access('xmpp', 'member')
	@Help('Forget a dictionary definition', usage='<term>')
	def cmdForget(self, muc, client, args, say, whisper):
		term = args[0].lower()

		current, scope = self._getDefinition(term, muc)
		if current is not None:
			if scope == 'global':
				say("The term %s is defined globally, use !forget-global" % term)
				return
			elif scope == 'private':
				say("The term %s is defined privately, use !forget-private" % term)
				return
		else:
			say("Unknown term: %s" % term)
			return

		self._dict.delete({'term': term, 'group': muc.data['group']})
		say("Forgot definition for %s" % term)
	
	@Command('forget-global', minArgs=1)
	@Access('xmpp', 'member')
	@Help('Forget a global dictionary definition', usage='<term>')
	def cmdForgetGlobal(self, muc, client, args, say, whisper):
		term = args[0].lower()

		current, scope = self._getDefinition(term, muc)
		current = self._dict.getOne({'term': term, 'room': '', 'group': ''})
		if current is None:
			say("The term %s is not defined globally" % term)
			return

		self._dict.delete({'term': term, 'group': '', 'room': ''})
		say("Forgot global definition for %s" % term)
	
	@Command('forget-private', minArgs=1)
	@Access('xmpp', 'member')
	@Help('Forget a private dictionary definition', usage='<term>')
	def cmdForgetPrivate(self, muc, client, args, say, whisper):
		term = args[0].lower()

		current, scope = self._getDefinition(term, muc)
		current = self._dict.getOne({'term': term, 'room': muc.getId()})
		if current is None:
			say("The term %s is not defined privately" % term)
			return

		self._dict.delete({'term': term, 'room': muc.getId()})
		say("Forgot private definition for %s" % term)
	
	@Command('definfo', minArgs=1)
	@Access('xmpp', 'moderator')
	@Help('Query information about a definition', usage='<term>')
	def cmdDefInfo(self, muc, client, args, say, whisper):
		term = (args[0])
		term = term.lower()

		entries = self._getDefinitions(term)
		for entry in entries:
			scope = ''
			if entry['room'] == '' and entry['group'] == '':
				scope = ' globally'
			elif entry['room'] != '' and entry['group'] == '':
				scope = ' privately'
			say('%s was defined%s by %s as "%s"' % (term,scope,  entry['author'], entry['def']))

		# replace with whisper once it's written

	def onRoomMessage(self, muc, client, message, jid=None):
		if message[0:1] != '?':
			return
		term = message.split(" ", 1)[0][1:].lower()

		current, scope = self._getDefinition(term, muc)
		if current is None:
			return

		muc.sendMessage(self.postProcess(current['def'], client))

	def postProcess(self, defin, client):
		return defin.replace("$who", client.getNick())
	
	def _getDefinition(self, term, muc):
		defs = self._getDefinitions(term)
		groupDef = None
		globalDef = None
		for entry in defs:
			if entry['group'] == '' and entry['room'] == '':
				globalDef = entry
			elif entry['group'] == muc.data['group']:
				groupDef = entry
			elif entry['room'] == muc.getId():
				return (entry, 'private')
		if groupDef is not None:
			return (groupDef, 'group')
		if globalDef is not None:
			return (globalDef, 'global')
		return (None, 'none')
	
	def _getDefinitions(self, term):
		return self._dict.get({'term': term})
