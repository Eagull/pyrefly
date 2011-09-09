import random
import xmppUtils
import urllib

commandText = 'quote'
helpText = 'Repeats a random quote.'
quote_file = 'commands/quotes.txt'

def process(sender, type, quote, client):
	room = sender.getStripped()
	quote = random.choice(open(quote_file).readlines()).strip()
	xmppUtils.sendMessage(room, quote, type='groupchat')
