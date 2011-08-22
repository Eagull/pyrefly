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
from libCommand import Dispatcher


class Dictionary(Plugin):
	
	def __init__(self):
		Plugin.__init__(self)
		self.dispatcher = Dispatcher()
		self.dispatcher.define('define', self.cmdDefine, access='member', args=2)
	
	def onLoad(self, bot):
		Plugin.onLoad(bot)
		self.dictionary = self.bot.db.table('dictionary')
	
	def cmdDefine(muc, client, args, respond):
		term, defin = args
		term = term.lower()
		
		entry = self.dictionary.get({'term': term, 'muc': muc.getId()})
		if entry is not None:
			respond("%s is already defined by %s: %s" % (term, entry['author'], entry['definition']))
			return
		
		self.dictionary.put({'term': term, 'muc': muc.getId(), 'author': client.getNick(), 'definition': defin)
		respond("Defined %s" % term)
		
	def onMucMessage(self, muc, client, message, jid=None)
		if self.dispatcher.onMucMessage(muc, client, message, jid=jid):
			return
		
		if message[0:1] != '!':
			return
		
		term = message.split(" ", 1)[0][1:].lower()
		
		entry = self.dictionary.getOne({'term': term, 'muc': muc.getId()})
		if not entry:
			return
		
		muc.sendMessage(self.postProcess(entry['definition'], client))
	
	def postProcess(self, defin, client):
		return defin.replace("%n", client.getNick())