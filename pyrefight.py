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
import re
#~ import xmppUtils

gdataclient = ''
SPREADSHEET_ID = config.get("SPREADSHEET_ID", "pyrefight")
NICK = config.get("NICK")

gdataclient = gdata.spreadsheet.service.SpreadsheetsService()
gdataclient.email = config.get("account", "pyrefight")
gdataclient.password = config.get("pass", "pyrefight")
gdataclient.source = NICK
gdataclient.ProgrammaticLogin()

fightdata = dict()

def presHandler(SENDER, PRES):
	try:
		jid = str(PRES.getJid())
	except UnicodeEncodeError:
		return -1
	try:
		jid = jid.split("/")[0]
	except AttributeError:
		return -2

	#~ print type(jid)
	if jid == 'None':
		#~ bot.client.UnregisterHandler('message', fightHandler.messageHandler)
		#~ bot.client.UnrgisterHandler('presence', pyrefight.presHandler)
		#~ xmppUtils.sendMessage(room, "PyreFight must be run as a moderator in order for it to work. Grant level of mod (or higher) and restart to reactivate", "groupchat")
		return -3

	if PRES.getRole() == "none":
		try:
			setstats(jid,fightdata[jid])
		except KeyError:
			getstats(jid) # This will set data if it does not exist.

	else:
		fightdata[jid] = getstats(jid)
	#~ print fightdata


#=============================================================================================================================

def getstats(WHO):
	if len(WHO) == 0:
		return -1

	DICT = dict()

	Q = gdata.spreadsheet.service.ListQuery()
	Q.sq = 'jid="' + WHO + '"'
	RESULTS = gdataclient.GetListFeed(SPREADSHEET_ID, 'od6', query=Q).entry
	if len(RESULTS) == 0: # Check for no RESULTS
		DICT = {'jid': WHO, 'level': 1, 'xp': 0, 'hp': 100+(1*9)*(1*6)/(1+(1*3)), 'maxhp': 100+(1*9)*(1*6)/(1+(1*3)), 'accuracy': 20, 'karma': 50, 'gold': 100, 'ammo': 20, 'timeout': time.time()}
		setstats(WHO,DICT)
		return DICT

	#write a bit of code to write the values to something everyware can access
	#~ print RESULTS[0].custom['points'].text
	DICT = {'jid': RESULTS[0].custom['jid'].text, 'level': int(RESULTS[0].custom['level'].text), 'xp': int(RESULTS[0].custom['xp'].text), 'hp': int(RESULTS[0].custom['hp'].text), 'maxhp': int(RESULTS[0].custom['maxhp'].text), 'accuracy': 38 + (int(RESULTS[0].custom['level'].text) * 2), 'karma': int(RESULTS[0].custom['karma'].text), 'gold': int(RESULTS[0].custom['gold'].text), 'ammo': int(RESULTS[0].custom['ammo'].text), 'timeout': time.time()}
	#~ print DICT
	return DICT

def setstats(WHO,DICT):
	if len(DICT) == 0 or len(WHO) == 0:
		return -1

	if re.match('[0-9]{26}@speeqe\.com', WHO) != None:
		return -2 # Let's not have it save randomly generated users. this will only effect people with no client and no account.


	WHAT = {} # define an array, format should have all items of a spreadsheet row
	WHAT['num'] = "=ROW()"
	WHAT['jid'] = WHO
	WHAT['level'] = str(DICT['level'])
	WHAT['hp'] = str(DICT['hp'])
	WHAT['maxhp'] = str(DICT['maxhp'])
	WHAT['xp'] = str(DICT['xp'])
	WHAT['karma'] = str(DICT['karma'])
	WHAT['gold'] = str(DICT['gold'])
	WHAT['ammo'] = str(DICT['ammo'])
	# Accuracy does not need to be stored as it is calculated off of LEVEL, 38 + level*2

	Q = gdata.spreadsheet.service.ListQuery()
	Q.sq = 'jid="' + WHO + '"'
	RESULTS = gdataclient.GetListFeed(SPREADSHEET_ID, 'od6', query=Q).entry
	if len(RESULTS) > 0:
		NUM = int(RESULTS[0].custom['num'].text)
		FEED = gdataclient.GetListFeed(SPREADSHEET_ID, 'od6')
		ENTRY = gdataclient.UpdateRow(FEED.entry[int(str(NUM - 2))], WHAT)
		if isinstance(ENTRY, gdata.spreadsheet.SpreadsheetsList):
			return 2
		return 0

	else:
		ENTRY = gdataclient.InsertRow(WHAT, SPREADSHEET_ID, 'od6')
		if isinstance(ENTRY, gdata.spreadsheet.SpreadsheetsList):
			return 1
		return 0