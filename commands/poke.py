import xmppUtils
import time
import random

commandText = 'poke'
helpText = 'Annoyingly autopoke someone.'

def process(sender, type, args, client):
	room = sender.getStripped()
	if len(args) == 0:
		xmppUtils.sendMessage(room, helpText, type='groupchat')
	elif len(args) > 0:
		room = sender.getStripped()
		poke = '/me pokes ' + args
		for i in range(1,random.randint(1,5)):
			xmppUtils.sendMessage(room, poke, type='groupchat')
			time.sleep(1)
