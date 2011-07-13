import random
import xmppUtils

commandText = 'shoot'
helpText = 'Has Yami shoot the member to whom you are referring.'

weapons = ["an FN SCAR", "an M4A1 SOPMOD", "an M16A2", "a Barrett M82", "an L86A1", "an M1903 Springfield", "a S&W .500", "a Dreyse Needle Gun", "an Advancement Armories Tesla Gun", "Two Slices of Very Sharp Toast", "a Big Bad Mother Fucking Gun (BBMFG)", "two more shots of tequila than he could handle", "some 22 caliber aspirin"]

def process(sender, type, args, client):
	comSend = sender.getResource()
	room = sender.getStripped()
	if len(args) == 0:
		xmppUtils.sendMessage(room, helpText, type='groupchat')
	elif len(args) >= 1 and args == ('himself', 'herself'):
	#~	xmppUtils.sendMessage(room, '/me shoots ' + comSend + ' in the back of the head.'
		xmppUtils.setRole(room, comSend, 'none', random.choice(['Ouch.', 'Suicide...', 'Wait, why?', 'Nice Kurt Cobain imitation.']))
	elif len(args) > 0:
		fire = '/me shoots at %s with %s' % (args, random.choice(weapons))
		randaim = random.randint(1,100)
		if (randaim >= 80):
			xmppUtils.sendMessage(room, fire, type='groupchat')
			xmppUtils.setRole(room, args, 'none', random.choice(['BOOM. Headshot.', 'Ouch, that\'s gotta hurt.', 'He wont be in Rush Hour Three...', '...that\'s gonna leave a bruise in the mornin\'.']))

		elif (randaim >= 30):
			xmppUtils.sendMessage(room, fire, type='groupchat')
			xmppUtils.setRole(room, args, 'visitor')
			xmppUtils.sendMessage(room, random.choice(['Ouch, that\'s gotta hurt.', '...that\'s gonna leave a bruise in the mornin\'.', '\'Tis but a flesh wound!']), type='groupchat')

		elif (randaim <= 15):
			xmppUtils.sendMessage(room, fire, type='groupchat')
			xmppUtils.sendMessage(room, 'My apologies, it appears I missed horridly. Try again later.', type='groupchat')

