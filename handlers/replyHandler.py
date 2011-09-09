import random
import xmppUtils
import config

response = [
	"What?", "Who, me?", "Forget about it.", "Intredasting.",
	"I don't know what to say.", "Really?", "I like you too.",
	"Yay!", "Wow.", "Sounds like fun.", "Please explain.",
	"Forget about it.", "Thank you.", "Dunno about that.",
	"I know nothing.", "Hmm.", "Why are you talking to me, cant you see I'm lurking?",
	"Me too", "Well that was random.", "Hold on...", "Let me look that up.",
	"I'm confused", "I guess.", "Meh.", "Perhaps.", "Should I be offended?",
	"What do you mean?", "What the...?", "Whatever.",
	"Your beans are chilled, sir. move along...", "Well diddle my dog!"
	]

def messageHandler(client, msg):
	room = msg.getFrom().getStripped()
	comSend = msg.getFrom().getResource()
	randanswer = random.choice(response)

	if config.get("nick", room) in msg.getBody():
		rnd = random.randint(1,5)
		if rnd != 3:
			xmppUtils.sendMessage(room, randanswer, type='groupchat')