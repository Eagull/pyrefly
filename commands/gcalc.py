import urllib, xmppUtils
 
commandText = 'calc'
helpText = 'Google calculator and conversions'
 
def process(sender, type, args, client):
        if len(args) > 0:
		room = sender.getStripped()
                req = urllib.quote(args)
                resp = urllib.urlopen('http://www.google.com/ig/calculator?json?hl=en&q=%s' % req)
                resp = resp.readline().split('",')[1][6:]
                if resp:
                        xmppUtils.sendMessage(room, resp, type)
                else:
                        xmppUtils.sendMessage(room, 'There was an error processing your request.', type)