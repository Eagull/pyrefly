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

import gdata.spreadsheet.service
import config
import time
import xmppUtils

gdataclient = ''
SPREADSHEET_ID = config.get("SPREADSHEET_ID", "dictionary")
WORKSHEET_ID = config.get("WORKSHEET_ID", "dictionary")
NICK = config.get("NICK")

gdataclient = gdata.spreadsheet.service.SpreadsheetsService()
gdataclient.email = config.get("account", "dictionary")
gdataclient.password = config.get("pass", "dictionary")
gdataclient.source = NICK
gdataclient.ProgrammaticLogin()

def process(SENDER, ARGS):
	tosay = 0
	try:
		str(ARGS)
		if len(ARGS) > 0:

			ROOM = SENDER.getStripped()
			NICK = SENDER.getResource()
			SPLIT = ARGS.split(" ", 2)
			CODE = len(SPLIT)



			# SPLIT[0] = learn, SPLIT[1] = TERM, SPLIT[2] = WHAT
			if CODE == 3 and SPLIT[0] == "learn":
				if SPLIT[1] == "splash":
					tosay = "Let me put it this way, I do not WANT to know splash"
				elif not xmppUtils.isMember(ROOM,NICK):
					tosay = "You are not allowed to teach me!"
				else:
					tosay = learn(SPLIT[1], SPLIT[2], NICK)
					if tosay == 1:
						tosay = "/me learned "+SPLIT[1]+"!"
					elif tosay == 2:
						tosay = "/me already knows "+SPLIT[1]+"!"
					elif tosay == 0:
						tosay = "Something went terribly wrong...."

			# This functionality will never be used, because it is deactivated in commandhandler line 50
			# SPLIT[0] = relearn, SPLIT[1] = TERM, SPLIT[2] = WHAT
			elif CODE == 3 and SPLIT[0] == "relearn": # this is a little redundant, as you could have it call learn on "redef" and "redefine" and it would do the same bloody thing
				#~ if not xmppUtils.isMember(ROOM,NICK):
					#~ tosay = "You are not allowed to change WHAT I know!"
				#~ else:
					tosay = relearn(SPLIT[1], SPLIT[2], NICK)
					if tosay == 1:
						tosay = "/me : Redefining "+SPLIT[1]+" since 1970."
					else:
						tosay = "Something went terribly wrong...."

			# SPLIT[0] = forget, SPLIT[1] = TERM, SPLIT[2] = (NA"garbage)
			elif CODE >= 2 and SPLIT[0] == "forget":
				#~ if not xmppUtils.isModerator(ROOM,NICK):
					#~ tosay = "You are not allowed to make me forget!"
				#~ else:
				if SPLIT[1] == "splash":
					tosay = "Gladly."
					forget(SPLIT[1])
				else:
					if forget(SPLIT[1]) == 1:
						tosay = "/me forgot "+SPLIT[1]+" D:"
					else:
						tosay = "Can't forget WHAT I don't know!"

			# SPLIT[0] = TERM, SPLIT[1] = (NA|garbage), SPLIT[2] = (NA{garbage)
			else:
				tosay = recall(SPLIT[0])
				if tosay == 0:
					tosay = "I do not know "+SPLIT[0]+"!"
				elif tosay == -1:
					tosay = 0

		elif len(ARGS) == 0:
			print len(ARGS)
			tosay = "If you would like me to recall something, type ? and then your query. Example: ?test\rYou may try this now"

	except UnicodeEncodeError:
		tosay = "Now now, let's not mess up our nice dictionary with your useless unicode blarky"

	if tosay <> 0:
		ROOM = SENDER.getStripped()
		xmppUtils.sendMessage(ROOM, tosay, type='groupchat')

#=============================================================================================================================

def recall(WHAT): # read the def for WHAT in the google spreadsheet
	if len(WHAT) == 0:
		return -1

	Q = gdata.spreadsheet.service.ListQuery()
	Q.sq = 'term="' + WHAT + '"'
	RESULTS = gdataclient.GetListFeed(SPREADSHEET_ID, WORKSHEET_ID, query=Q).entry
	if len(RESULTS) == 0: # Check for no RESULTS
		#~ return WHAT + " is not defined!"
		return 0

	READABLETIME = time.ctime(float(RESULTS[0].custom['created'].text)/1000)
	#~ s = "%s: %s\r(%s - %s)" % (RESULTS[0].custom['term'].text, RESULTS[0].custom['def'].text, RESULTS[0].custom['author'].text, READABLETIME)
	s = "%s" % (RESULTS[0].custom['def'].text)
	return s

def learn(TERM, DEFINITION, WHO): # adds or replaces a TERM in the dictionary
	if len(TERM) == 0 or len(DEFINITION) == 0 or len(WHO) == 0:
		return -1

	DEFINITION = cleanstring(DEFINITION)

	Q = gdata.spreadsheet.service.ListQuery()
	Q.sq = 'term="' + TERM + '"'
	RESULTS = gdataclient.GetListFeed(SPREADSHEET_ID, WORKSHEET_ID, query=Q).entry
	if len(RESULTS) > 0: # If it exists, pass the number of line to update()
		#~ NUM = int(RESULTS[0].custom['num'].text) # requested we save this for a later date...
		#~ CREATED = RESULTS[0].custom['created'].text
		#~ AUTHOR = RESULTS[0].custom['author'].text
		#~ return relearn(TERM, DEFINITION, WHO, NUM, CREATED, AUTHOR)
		return 2

	WHAT = {} # define an array, format should have all items of a spreadsheet row
	WHAT['term'] = TERM
	WHAT['def'] = DEFINITION
	WHAT['author'] = WHO
	WHAT['created'] = str(time.time()*1000) # For some odd reason, thease values are stored as value * 1000 in the dictionary O.o
	WHAT['num'] = '=ROW()-1' # changeing this one will break the delete and remember function

	ENTRY = gdataclient.InsertRow(WHAT, SPREADSHEET_ID, WORKSHEET_ID)
	if isinstance(ENTRY, gdata.spreadsheet.SpreadsheetsList):
		return 1
	return 0

def relearn(TERM, DEFINITION, WHO, NUM = -1, CREATED = -1, AUTHOR = -1): # This function RE-STATES an EXISTING def. This replaces (!forget <n>, !def <n> = blarky)
	if len(TERM) == 0 or len(DEFINITION) == 0 or len(WHO) == 0:
		return -1

	DEFINITION = cleanstring(DEFINITION)

	if NUM == -1:
		Q = gdata.spreadsheet.service.ListQuery()
		Q.sq = 'term="' + TERM + '"'
		RESULTS = gdataclient.GetListFeed(SPREADSHEET_ID, WORKSHEET_ID, query=Q).entry
		if len(RESULTS) == 0: # Check for no RESULTS
			#~ return WHAT + " is not defined!"
			return learn(TERM, DEFINITION, WHO)
		NUM = int(RESULTS[0].custom['num'].text)
		CREATED = RESULTS[0].custom['created'].text
		AUTHOR = RESULTS[0].custom['author'].text
	#~ print NUM
	WHAT = {}
	WHAT['term'] = TERM
	WHAT['def'] = DEFINITION
	WHAT['created'] = CREATED
	WHAT['author'] = AUTHOR
	WHAT['editor'] = WHO
	WHAT['modifyed'] = str(time.time()*1000)
	WHAT['num'] = '=ROW()-1' # changeing this one will break the delete and remember function

	FEED = gdataclient.GetListFeed(SPREADSHEET_ID, WORKSHEET_ID)
	ENTRY = gdataclient.UpdateRow(FEED.entry[int(str(NUM - 1))], WHAT)
	if isinstance(ENTRY, gdata.spreadsheet.SpreadsheetsList):
		#~ print 'Updated ' + TERM + '!'
		return 1
	return 0

def forget(TERM):
	Q = gdata.spreadsheet.service.ListQuery()
	Q.sq = 'term="' + TERM + '"'
	RESULTS = gdataclient.GetListFeed(SPREADSHEET_ID, WORKSHEET_ID, query=Q).entry
	try:
		NUM = int(RESULTS[0].custom['num'].text)
	except IndexError:
		return 0
	#~ print NUM
	FEED = gdataclient.GetListFeed(SPREADSHEET_ID, WORKSHEET_ID)
	ENTRY = gdataclient.DeleteRow(FEED.entry[int(str(NUM - 1))])
	#~ print 'Forgot ' + TERM
	return 1

def cleanstring(s): # CLEANING STRING PREVENTS FORMULA DATATYPE ERRORS
	if s[:1] == "=":
		s = s[1:]
	if s[:1] == ">":
		s = s[1:]
	if s[:1] == "<":
		s = s[1:]
	if s[:1] == " ":
		s = s[1:]
	return s
