import xmppUtils
from xgoogle.translate import Translator, TranslationError

commandText = 'tr'
helpText = 'Translates from one language to english.'

def process(sender, args, type, client):
	args = args.split(' ',2)
	action = args[0]
	room = sender.getStripped()
	translate = Translator().translate
	translatePhrase = ("%s" %(args))
	if action > 1:
		translation = translate(translatePhrase, action)
		xmppUtils.sendMessage(room, translation, type='groupchat')