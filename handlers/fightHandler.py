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

import pyrefight
import xmppUtils
import random
import time
from decimal import *


def messageHandler(client, msg):
	# TODO: ignore messages from self

	data = msg.getBody()
	try:
		data = data.split(" ",4)
	except AttributeError:
		return 1

	if data and len(data) >= 3 and data[0] == '/me':

		room = msg.getFrom().getStripped()
		nick = msg.getFrom().getResource()
		target = data[2]
		targetJID = room+"/"+target
		nickJID = room+"/"+nick

		try:
			nickJID = xmppUtils.rosters[room][nick][2]
		except KeyError:
			return 0
		try:
			nickJID = str(nickJID)
		except UnicodeEncodeError:
			return -1
		try:
			nickJID = nickJID.split("/")[0]
		except AttributeError:
			return -2

		if data[1].lower() == "revives" or data[1].lower() == "shoots" or data[1].lower() == "heals" or data[1].lower() == "gives":
			try:
				targetJID = xmppUtils.rosters[room][target][2]
			except KeyError:
				xmppUtils.sendMessage(room+"/"+nick, "Target does not exist!", "private")
				return 0
			try:
				targetJID = str(targetJID)
			except UnicodeEncodeError:
				return -1
			try:
				targetJID = targetJID.split("/")[0]
			except AttributeError:
				return -2

		if targetJID == 'None' or nickJID == 'None':
			#~ client.RegisterHandler('message', fightHandler.messageHandler)
			#~ client.RegisterHandler('presence', pyrefight.presHandler)
			#~ xmppUtils.sendMessage(room, "PyreFight must be run as a moderator in order for it to work. Grant level of mod (or higher) and restart to reactivate", "groupchat")
			return -3

		#	#	#	#	#	SHOOTING 	#	#	#	#	#
		if len(data) >= 3 and data[1].lower() == "shoots":
			if pyrefight.fightdata[nickJID]['hp'] <= 0:
				xmppUtils.sendMessage(room+"/"+nick, "You're a bloody corpse. This is no time to be shooting people!", "private")
			elif pyrefight.fightdata[nickJID]['ammo'] >= 1:
				mod = (40-pyrefight.fightdata[nickJID]['karma'])/10
				if mod < -1: mod = -1
				if time.time() < 2+pyrefight.fightdata[nickJID]['timeout']:
					return -4
				pyrefight.fightdata[nickJID]['timeout'] = time.time()
				pyrefight.fightdata[nickJID]['ammo'] -= 1

				shot = random.randint(1, 100)
				if pyrefight.fightdata[targetJID]['hp'] <= 0: shot = shot/2
				if shot < pyrefight.fightdata[nickJID]['accuracy'] and shot != 4: # The higher the accuracy, the easyer for shot to be under it and therefore the more often it hits
					damage = random.randint(10+(pyrefight.fightdata[nickJID]['level']/4), 19+(pyrefight.fightdata[nickJID]['level']/2))
					if int(pyrefight.fightdata[targetJID]['hp']) <= 0:
						pyrefight.fightdata[nickJID]['xp'] += 1 # add exp
						xmppUtils.sendMessage(room+"/"+nick, "You shot "+target+"'s bloody corpse. yay......", "private")

					elif int(pyrefight.fightdata[targetJID]['hp']) - damage <= 0:
						pyrefight.fightdata[nickJID]['xp'] += 25+(pyrefight.fightdata[targetJID]['maxhp']/2) # add exp, If below 0 (overkill) give bonus exp
						pyrefight.fightdata[nickJID]['karma'] -= 5 # remove 5 karma
						pyrefight.fightdata[nickJID]['gold'] += 25+(pyrefight.fightdata[targetJID]['maxhp']/3) # add gold

						pyrefight.fightdata[targetJID]['hp'] = 0 # set health to 0 (dead)
						pyrefight.fightdata[targetJID]['xp'] -= 10 # remove xp
						pyrefight.fightdata[targetJID]['karma'] += 3 # add 3 karma
						if pyrefight.fightdata[targetJID]['karma'] > 100: pyrefight.fightdata[targetJID]['karma'] = 100
						if pyrefight.fightdata[targetJID]['xp'] < 0: pyrefight.fightdata[targetJID]['xp'] = 0 # make xp 0 if it's below zero

						xmppUtils.sendMessage(room+"/"+target, nick+" killed you D: You lost 10 xp.", "private")
						xmppUtils.sendMessage(room+"/"+nick, "You shoot and kill "+target+"! "+str(((damage/5)*4) - (pyrefight.fightdata[targetJID]['hp']*4))+"xp gained, "+str(pyrefight.fightdata[targetJID]['maxhp'])+" gold gained", "private")
						xmppUtils.sendMessage(room, nick+" has killed "+target+" D:", "groupchat")

					else:
						pyrefight.fightdata[nickJID]['xp'] += ((damage/3)*4) # add exp
						pyrefight.fightdata[nickJID]['gold'] += damage/pyrefight.fightdata[nickJID]['level'] # add gold
						pyrefight.fightdata[targetJID]['hp'] -= damage # remove health

						xmppUtils.sendMessage(room+"/"+target, nick+"'s shot hit you! "+str(pyrefight.fightdata[targetJID]['hp'])+"/"+str(pyrefight.fightdata[targetJID]['maxhp'])+" hp left, "+str(damage)+" hp lost.", "private")
						xmppUtils.sendMessage(room+"/"+nick, "You shot "+target+" ("+str(pyrefight.fightdata[targetJID]['hp'])+"/"+str(pyrefight.fightdata[targetJID]['maxhp'])+" hp). "+str(damage)+" damage dealt, "+str((damage/3)*4)+" xp gained", "private")

				else:
					if pyrefight.fightdata[targetJID]['hp'] <= 0:
						xmppUtils.sendMessage(room+"/"+nick, "You missed "+target+"'s corpse. Damn you suck :P", "private")
					else:
						xmppUtils.sendMessage(room+"/"+nick, "You missed "+target+" you dolt!", "private")
						xmppUtils.sendMessage(room+"/"+target, nick+" shot at you, and missed! Shoot that bugger back :P", "private")

				checklvlup(nickJID, nick, room)

			else:
				xmppUtils.sendMessage(room+"/"+nick, "You have no ammo left!", "private")

		#	#	#	#	#	 buying 	#	#	#	#	#
		elif len(data) >= 3 and data[1].lower() == "buys":
			num = 0
			#~ print data
			try:
				num = int(data[2])
			except ValueError:
				if data[2] == 'max':
					if data[3].lower() == "ammo" or data[3].lower() == "bullets": num = pyrefight.fightdata[nickJID]['gold']/5
					if data[3].lower() == "hp" or data[3].lower() == "health": num = pyrefight.fightdata[nickJID]['gold']/3
				else:
					xmppUtils.sendMessage(room+"/"+nick, "Syntax is '/me buys n object'. You must use 'bullets', 'ammo', 'hp', 'health' for object, and supply an integer, or the word 'max' for n.", "private")
					return 1

			if num < 0:
				xmppUtils.sendMessage(room+"/"+nick, "Cannot use amounts below 0", "private")
				return -1

			if data[3].lower() == "ammo" or data[3].lower() == "bullets":
				if  pyrefight.fightdata[nickJID]['gold'] < 5*num:
					xmppUtils.sendMessage(room+"/"+nick, "Insufficient gold!", "private")
				else:
					pyrefight.fightdata[nickJID]['gold'] -= 5*num
					pyrefight.fightdata[nickJID]['ammo'] += num

					xmppUtils.sendMessage(room, "/me takes "+str(5*num)+" gold from and gives "+str(num)+" bullets to "+nick, "groupchat")

			elif data[3].lower() == "health" or data[3].lower() == "hp":
				if num + pyrefight.fightdata[nickJID]['hp'] > pyrefight.fightdata[nickJID]['maxhp']:
					num = pyrefight.fightdata[nickJID]['maxhp'] - pyrefight.fightdata[nickJID]['hp']

				if pyrefight.fightdata[nickJID]['gold'] < 3*num:
					xmppUtils.sendMessage(room+"/"+nick, "Insufficient gold!", "private")
					#~ print 3*num
					#~ print pyrefight.fightdata[nickJID]['gold']

				else:
					pyrefight.fightdata[nickJID]['gold'] -= 3*num
					pyrefight.fightdata[nickJID]['hp'] += num
					xmppUtils.sendMessage(room, "/me takes "+str(3*num)+" gold from and heals "+str(num)+" hp for "+nick, "groupchat")

		#	#	#	#	#	 Revive 	#	#	#	#	#
		elif len(data) >= 3 and data[1].lower() == "revives":
			if pyrefight.fightdata[targetJID]['hp'] == 0 and pyrefight.fightdata[nickJID]['hp'] > 0:
				pyrefight.fightdata[nickJID]['hp'] -= pyrefight.fightdata[nickJID]['hp']/4
				pyrefight.fightdata[nickJID]['karma'] += 1
				pyrefight.fightdata[nickJID]['gold'] += 25
				pyrefight.fightdata[targetJID]['hp'] = pyrefight.fightdata[targetJID]['maxhp']/2
				xmppUtils.sendMessage(room+"/"+target, nick+" revived you! How nice :P", "private")
				xmppUtils.sendMessage(room+"/"+nick, "You revived "+target+" to half health! (and suffered "+str(pyrefight.fightdata[nickJID]['hp']/4)+" damage for it)", "private")
				xmppUtils.sendMessage(room, nick+" gave a quarter of their hp to give "+target+" half of theirs. How noble.", "groupchat")

		#	#	#	#	#	  heal  	#	#	#	#	#
		elif len(data) >= 3 and data[1].lower() == "heals":
			if pyrefight.fightdata[targetJID]['hp'] != 0 and pyrefight.fightdata[nickJID]['hp'] > 0 and nickJID <> targetJID and pyrefight.fightdata[targetJID]['maxhp'] != pyrefight.fightdata[targetJID]['hp']:
				amt = pyrefight.fightdata[nickJID]['hp']/10
				pyrefight.fightdata[nickJID]['hp'] -= amt
				if amt > 25: pyrefight.fightdata[nickJID]['karma'] += 1
				pyrefight.fightdata[nickJID]['gold'] += 5
				pyrefight.fightdata[targetJID]['hp'] += amt*3*(1+(pyrefight.fightdata[nickJID]['karma']-50))
				if pyrefight.fightdata[targetJID]['hp'] > pyrefight.fightdata[targetJID]['maxhp'] or pyrefight.fightdata[targetJID]['hp'] < 0:
					pyrefight.fightdata[targetJID]['hp'] = pyrefight.fightdata[targetJID]['maxhp']
				xmppUtils.sendMessage(room+"/"+target, nick+" healed you! "+str(amt*3)+" health restored", "private")
				xmppUtils.sendMessage(room+"/"+nick, "You healed "+target+" "+str(amt*3)+" hp! (and suffered "+str(amt)+" damage for it)", "private")
				#~ xmppUtils.sendMessage(room, nick+" gave "+str(amt)+" hp to heal "+target+" "+str(amt*3)+" of theirs.", "groupchat")

		#	#	#	#	#	  check 	#	#	#	#	#
		elif len(data) >= 3 and data[1].lower() == "checks" and "stats" in data:
			xmppUtils.sendMessage(room+"/"+nick,"Stats for "+str(pyrefight.fightdata[nickJID]['jid'])+" are:\rLevel:	"+str(pyrefight.fightdata[nickJID]['level'])+"\rHp:		"+str(pyrefight.fightdata[nickJID]['hp'])+"/"+str(pyrefight.fightdata[nickJID]['maxhp'])+"\rXp: 		"+str(pyrefight.fightdata[nickJID]['xp'])+"/"+str((11+pyrefight.fightdata[nickJID]['level'])*(12+pyrefight.fightdata[nickJID]['level']))+"\rAccuracy: 	"+str(pyrefight.fightdata[nickJID]['accuracy'])+"\rGold:	"+str(pyrefight.fightdata[nickJID]['gold'])+"\rKarma:	"+str(pyrefight.fightdata[nickJID]['karma'])+"/100\rAmmo:	"+str(pyrefight.fightdata[nickJID]['ammo']), 'private')

		#	#	#	#	#	  check 	#	#	#	#	#
		elif len(data) >= 3 and data[1].lower() == "checks" and "roster" in data and nick == "Corgano":
			xmppUtils.sendMessage(room+"/"+nick,pyrefight.fightdata, 'private')

		#	#	#	#	#	   save 	#	#	#	#	#
		elif len(data) >= 3 and data[1].lower() == "saves" and nick == "Corgano":
			for jid in pyrefight.fightdata:
				print jid
				pyrefight.setstats(jid,pyrefight.fightdata[jid])
			xmppUtils.sendMessage(room, "Data saved!", "groupchat")

		#	#	#	#	#	   give 	#	#	#	#	#
		elif len(data) >= 4 and data[1].lower() == "gives":
			try:
				num = int(data[3])
			except ValueError:
				xmppUtils.sendMessage(room+"/"+nick, "Syntax is '/me gives who n item'. You must supply a valid name for who, an integer for n, and one of the phrases 'bullets', 'ammo', 'gold' for item", "private")
				return 1

			if num < 0:
				xmppUtils.sendMessage(room+"/"+nick, "Cannot use amounts below 0", "private")
				return -1

			if data[4] == "bullets" or data[4] == "ammo":
				if num > pyrefight.fightdata[nickJID]['ammo']:
					xmppUtils.sendMessage(room+"/"+nick, "You havn't "+str(num)+" bullets to give!", "private")
					return 2
				pyrefight.fightdata[nickJID]['ammo'] -= num
				pyrefight.fightdata[targetJID]['ammo'] += num
				if num > 30: pyrefight.fightdata[nickJID]['karma'] += 1

			elif data[4] == "gold":
				if num > pyrefight.fightdata[nickJID]['gold']:
					xmppUtils.sendMessage(room+"/"+nick, "You havn't "+str(num)+" bullets to give!", "private")
					return 2
				pyrefight.fightdata[nickJID]['gold'] -= num
				pyrefight.fightdata[targetJID]['gold'] += num
				if num > 200: pyrefight.fightdata[nickJID]['karma'] += 1

			else:
				xmppUtils.sendMessage(room+"/"+nick, "Syntax is '/me gives who n item'. You must supply a valid name for who, an integer for n, and one of the phrases 'bullets', 'ammo', 'gold' for item", "private")

			xmppUtils.sendMessage(room+"/"+nick, target+" has recieved "+str(num)+" "+data[4]+" from you.", "private")
			xmppUtils.sendMessage(room+"/"+target, "You have recieved "+str(num)+" "+data[4]+" from "+nick+".", "private")



def checklvlup(nickJID, nick, room):
	level = pyrefight.fightdata[nickJID]['level']

	# amt is the amount of HP at the NEXT level. This times (level / 10) is the xp required
	amt = 100+(level*9)*(level*6)/(1+(level*3))
	if float(pyrefight.fightdata[nickJID]['xp']) > amt*(1+(level/10)):
		pyrefight.fightdata[nickJID]['xp'] -= amt*(1+(level/10))

		pyrefight.fightdata[nickJID]['level'] += 1
		# add the difference between the old max HP and the new one
		pyrefight.fightdata[nickJID]['hp'] += amt-(pyrefight.fightdata[nickJID]['maxhp'])
		pyrefight.fightdata[nickJID]['maxhp'] = amt
		pyrefight.fightdata[nickJID]['accuracy'] = 38 + (level * 2)
		pyrefight.fightdata[nickJID]['gold'] += 2*(amt-100)
		pyrefight.fightdata[nickJID]['ammo'] += 10+(level/2)
		print level
		xmppUtils.sendMessage(room+"/"+nick, "Congratulations! You are now level "+str(level+1)+"! You have been awarded "+str(2*(amt-100))+" gold and "+str(8*level)+" bullets.", "private")
		xmppUtils.sendMessage(room, nick+" has leveled up to level "+str(level)+".", "groupchat")

