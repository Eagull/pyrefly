import xmppUtils
from xgoogle.search import GoogleSearch, SearchError

commandText = 'google'
helpText = 'Returns the top result of a searched term.'

def process(sender, type, args, client):
        if len(args) > 0:
                room = sender.getStripped()
                gs = GoogleSearch(args)
                gs.results_per_page = 1
                results = gs.get_results()
                try:
                        msg = results[0].title.encode('utf8'), results[0].desc.encode('utf8'), results[0].url.encode('utf8')
                        xmppUtils.sendMessage(room, msg, type='groupchat')
                except KeyError or SearchError or IndexError:
                        xmppUtils.sendMessage(room, 'Search failed', type='groupchat')

        elif len(args) == 0:
                room = sender.getStripped()
                xmppUtils.sendMessage(room, helpText, type='groupchat')