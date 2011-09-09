import random
import xmppUtils
import rndobj

commandText = 'slap'
helpText = 'Slap the user to whom you are referring.'

rndobjects = rndobj.list

def process(sender, type, args, client):
  room = sender.getStripped()
  target = args
  if len(args) == 0:
    xmppUtils.sendMessage(room, helpText, type='groupchat')
  elif len(args) > 0:
    room = sender.getStripped()
    slap = '/me slaps ' + target + ' with ' + random.choice(rndobjects)
    xmppUtils.sendMessage(room, slap, type='groupchat')

