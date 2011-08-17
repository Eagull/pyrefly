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

import xmpp
import config

import xmppUtils
from handlers import commandHandler, logHandler, fightHandler, swearHandler, replyHandler
import pyrefight
import dictionary

# TODO: add SIGINT and exit handlers

class Pyrefly(object):

  def __init__(self, config):
    self.config = config
    self.jid = xmpp.JID(config.get('id'))
    self.client = xmpp.Client(self.jid.getDomain(), debug=[])
    self.handlers = list()
  
  def connect(self):
    connResult = self.client.connect()
    if not connResult:
      print "Error connecting to server: %s" % jid.getDomain()
      exit(2)
    
    resource = 'bot' + self.config.hash[:6]
    connResult = self.client.auth(jid.getNode(), self.config.get('password'), resource)
    if not connResult:
      print "Error authenticating user: %s" % jid.getNode()
      exit(3)
    
  def joinConfiguredRooms(self):
    self.client.sendInitPresence()
    self.client.RegisterHandler('presence', self.onPresence)
    self.client.RegisterHandler('message', self.onMessage)
  
    for room in config.getRoomList():
      self.join(room, config.get('nick', room))
  
  def join(self, room, nick):
    self.xmppUtil.joinMUC(nick, room)
  
  def process(self, timeout=0.1):
    return self.client.Process(timeout)
    
  def onPresence(self, *args, **kwargs):
    for handler in self.handlers:
      handler.onPresence(*args, **kwargs)
  
  def onMessage(self, *args, **kwargs):
    for handler in self.handlers:
      handler.onMessage(*args, **kwargs)
    
  def onRoster(self, *args, **kwargs):
    for handler in self.handlers:
      handler.onRoster(*args, **kwargs)
    pass
    
  def registerHandler(self, handler):
    handler.onRegister()
    self.handlers.append(handler)

##~ client.RegisterHandler('message', logHandler.messageHandler)
#client.RegisterHandler('presence', logHandler.presenceHandler)
#client.RegisterHandler('presence', xmppUtils.rosterHandler)
#client.RegisterHandler('message', commandHandler.messageHandler)

#client.RegisterHandler('message', replyHandler.messageHandler)
#client.RegisterHandler('message', swearHandler.messageHandler)

#client.RegisterHandler('message', fightHandler.messageHandler)
#client.RegisterHandler('presence', pyrefight.presHandler)

if __name__ == '__main__':
  pyrefly = Pyrefly()
  try:
    while pyrefly.process():
      pass
  except KeyboardInterrupt:
    exit(0)