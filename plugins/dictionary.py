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

#TODO: add date to defs

class Dictionary(Plugin):

	def __init__(self):
		Plugin.__init__(self)
		
	def onLoad(self, bot):
		Plugin.onLoad(self, bot)
		self.dictionary = self.bot.db.table('dictionary')
	
	@Command('learn', minArgs=2, maxArgs=2)
	@Help('Learn a new dictionary definition', usage='<term> <definition>')
	def cmdDefine(self, muc, client, args, say, whisper):
		term, defin = (args[0], args[1])
		term = term.lower()

		if len(defin) > 3 and defin[0:3] == '=> ':
			defin = defin[3:].trim()
		entry = self.dictionary.getOne({'term': term, 'muc': muc.getId()})
		if entry is not None:
			say("%s is already defined by %s: %s" % (term, entry['author'], entry['definition']))
			return

		self.dictionary.put({'term': term, 'muc': muc.getId(), 'author': client.getNick(), 'definition': defin})
		say("Defined %s" % term)
	
	@Command('forget', minArgs=1)
	@Help('Forget a dictionary definition', usage='<term>')
	def cmdForget(self, muc, client, args, say, whisper):
		term = args[0]
		termQuery = {'term': term.lower(), 'muc': muc.getId()}

		entry = self.dictionary.getOne(termQuery)
		if entry is None:
			say("Unknown term: %s" % term)
			return

		self.dictionary.delete(termQuery)
		say("Forgot %s" % term)

	@Command('definfo', minArgs=1)
	@Help('Query information about a definition', usage='<term>')
	def cmdDefInfo(self, muc, client, args, say, whisper):
		term = (args[0])
		term = term.lower()

		entry = self.dictionary.getOne({'term': term, 'muc': muc.getId()})
		if not entry:
			entry = self.dictionary.getOne({'term': term})
			if not entry:
				return

		# replace with whisper once it's written
		say('%s was defined by %s as "%s" in %s' % (term, entry['author'], entry['definition'], entry['muc']))

	def onMucMessage(self, muc, client, message, jid=None):
		if message[0:1] != '?':
			return
		term = message.split(" ", 1)[0][1:].lower()

		entry = self.dictionary.getOne({'term': term, 'muc': muc.getId()})
		if not entry:
			entry = self.dictionary.getOne({'term': term})
			if not entry:
				return

		muc.sendMessage(self.postProcess(entry['definition'], client))

	def postProcess(self, defin, client):
		return defin.replace("$who", client.getNick())
