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

import commands
import xmppUtils
import dictionary
from commands import *

commandMap = {}

for commandClassName in commands.__all__:
	command = getattr(commands, commandClassName)
	commandMap[command.commandText] = command

def messageHandler(client, msg):
	# TODO: ignore messages from self

	data = msg.getBody()
#	nick = msg.getFrom().getResource()

#	if not nick:
#		return

	# TODO: commandList = starting with NICK or '!' or private messages

	# TODO: Handle !help here - !help is a command
	# xmppUtils.sendMessage(sender, command.helpText, type)

	if data and len(data) >= 2 and data[0] == '!':
		argSplit = data[1:].split(' ', 1)
		command = argSplit[0].lower()
		args = argSplit[1] if len(argSplit) == 2 else '';
		if command in commandMap:
			# TODO: check authorization for given command
			# Now ignores devoiced users
			if xmppUtils.rosters[msg.getFrom().getStripped()][msg.getFrom().getResource()][1] <> 'visitor':
				commandMap[command].process(msg.getFrom(), msg.getType(), args, client);

		elif command == "learn" or command == "forget" or command == "relearn": # uncomment this last bit to ENABLE relearning
			dictionary.process(msg.getFrom(), data[1:])

	elif data and len(data) >= 2 and data[0] == '?': # THIS IS FOR DICT FUNCS (namely recall)
		dictionary.process(msg.getFrom(), data[1:]);


