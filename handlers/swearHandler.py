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

import random
import xmppUtils
import config

badwords = ['bitch', 'fuck', 'jesu cristo', 'asshole', 'republican', 'democrat', 'shit', 'cunt', 'whore', 'slut', 'faggot']
advwords = {'cock': "* By that I mean chicken", 'George Bush' : "* By that I mean chicken", 'madre de dios': "You're the bitch, bitch!"}

def messageHandler(client, msg):
	room = msg.getFrom().getStripped()
	comSend = msg.getFrom().getResource()

	if config.get("nick") == comSend: return 0

	for word in badwords:
		try:
			if word.lower() in msg.getBody().lower():
				if random.randint(1,2) == 1: # The higher the second number is, the less chance of getting kicked but greater chance fo getting devoiced
					xmppUtils.sendMessage(room,'/me slaps ' + comSend + ' around a while, then hastily shows them the door.','groupchat')
					xmppUtils.setRole(room, comSend, 'none', 'Watch your language!')
					return 1

				else:
					xmppUtils.sendMessage(room,'/me rips out ' + comSend + "'s voice and beats him with it",'groupchat')
					xmppUtils.setRole(room, comSend, 'visitor')
					return 1
		except AttributeError:
			return 0

	for word in advwords:
		try:
			if word.lower() in msg.getBody().lower():
				xmppUtils.sendMessage(room, advwords[word],'groupchat')

		except AttributeError:
			return 0