import random
import xmppUtils
import rndobj

commandText = 'gift'
helpText = 'Give the user to whom you are referring a gift.'

rndobjects = rndobj.list

def process(sender, type, args, client):
  room = sender.getStripped()
  if len(args) == 0:
    xmppUtils.sendMessage(room, helpText, type='groupchat')
  elif len(args) > 0:
    room = sender.getStripped()
    gift = '/me opens up a box and gives ' + args + ' ' + random.choice(rndobjects)
    xmppUtils.sendMessage(room, gift, type='groupchat')

