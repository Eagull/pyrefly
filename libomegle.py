# Omegle-XMPP
# Copyright (C) 2010 The Omegle-XMPP team

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from threading import Lock, Thread
import config
import re
import urllib
import urllib2
import gzip
import StringIO

try:
    import simplejson # python2.5
    json = simplejson
except:
    try:
        import json
    except:
        print "NO JSON LIBRARY"
        pass

class OmegleConnection:
    sid = ''
    url = config.get("server", "omegle")

    def __init__(self):
        pass

    def _post_req(self, url, params='', jsonenc=False):
        req = urllib2.Request(self.url + url)
        req.add_header("Content-type", "application/x-www-form-urlencoded; charset=utf-8")
        req.add_header("Accept", "*/*")
        try:
            res = urllib2.urlopen(req, params)
            data = res.read()

            if jsonenc:
                data = json.loads(data)

            return data
        except:
            return 'error'

    def join(self):
        data = self._post_req("/start?rcs=1&spid=", '', True)
        if data != 'error':
            self.sid = data
            return 1

        return 0

    def send(self, msg, encode=True):
        params = ''

        if encode:
            params = urllib.urlencode({'msg': msg, 'id': self.sid})
        else:
            params = 'msg=%s&%s' % (msg, urllib.urlencode({'id': self.sid}))

        data = self._post_req('/send', params, False)

        if data == "win":
            return 1

        return 0

    def getEvent(self):
        params = urllib.urlencode({'id': self.sid})
        data = self._post_req('/events', params, True)
        return data

    def leave(self):
        params = urllib.urlencode({'id': self.sid})
        data = self._post_req('/disconnect', params, True)
        return data

    def getsid(self):
        return self.sid

    def setsid(self, sid):
        self.sid = sid

    def captchaGetID(self, code):
        parameters = "/recaptcha/api/challenge?k=%s&ajax=1&cachestop=0.7569315146943529" % code
        req = urllib2.Request("http://www.google.com" + parameters)
        req.add_header("Accept-encoding", "gzip")

        try:
            res = urllib2.urlopen(req)
            data = res.read()
            if res.headers.get('content-encoding', None) == 'gzip':
                data = gzip.GzipFile(fileobj=StringIO.StringIO(data)).read()
            return re.search("challenge : '(.+?)'", data).group(1)
        except:
            return "-1"

    def captchaConfirm(self, id, response):
        params = urllib.urlencode({'id': self.sid, 'challenge': id, 'response': response})
        data = self._post_req('/recaptcha', params)
        if data == 'win':
            return 1

        return 0

class ConnThread(Thread):
    msgs = []
    msgs_mutex = Lock()
    discreq = False
    discreq_mutex = Lock()
    debug = False

    def __init__(self, debug=False):
        self.debug = debug
        Thread.__init__(self)

    def run(self):
        self.omeglecon = OmegleConnection()
        self.omeglecon.join()
        connected = True

        while connected:
            self.discreq_mutex.acquire()
            tmp = self.discreq
            self.discreq_mutex.release()

            if tmp:
                break

            events = self.omeglecon.getEvent()
            if self.debug:
                print events
            tmp = []

            if events == None:
                continue

            for event in events:
                if event[0] == 'waiting':
                    pass

                elif event[0] == 'connected':
                    tmp.append([event[0], self.omeglecon.getsid()])

                elif event[0] == 'gotMessage':
                    tmp.append(event)

                elif event[0] == 'typing':
                    pass

                elif event[0] == 'stoppedTyping':
                    pass

                elif event[0] == 'strangerDisconnected':
                    tmp.append(event)
                    connected = False

                elif event[0] == 'recaptchaRequired':
                    tmp.append([event[0], self.omeglecon.getsid(), event[1]])

                elif event[0] == 'recaptchaRejected':
                    tmp.append(event)

            self.msgs_mutex.acquire()
            self.msgs += tmp
            self.msgs_mutex.release()

    def getMessages(self):
        tmp = []

        self.msgs_mutex.acquire()
        tmp = self.msgs
        self.msgs = []
        self.msgs_mutex.release()

        return tmp

    def setDiscRequest(self):
        self.discreq_mutex.acquire()
        self.discreq = True
        self.discreq_mutex.release()

class SendThread(Thread):
    def __init__(self, sid, type, msg1='', msg2=''):
        Thread.__init__(self)

        self.omeglecon = OmegleConnection()
        self.omeglecon.setsid(sid)
        self.type = type
        self.msg1 = msg1
        self.msg2 = msg2

    def run(self):
        if self.type == 'message':
            self.omeglecon.send(self.msg1)
        elif self.type == 'captcha':
            self.omeglecon.captchaConfirm(self.msg1, self.msg2)
        else:
            self.omeglecon.leave()

class Omegle:
    hooks = {}
    conthr = None
    sid = ''
    connected = False
    captchaid = ''
    debug = False

    def __init__(self, debug=False):
    	self.debug = debug
        pass

    def registerHook(self, name, func):
        dbn = ['join', 'leave', 'message', 'captchaRequired', 'captchaRejected']
        if name in dbn:
            self.hooks[name] = func

    def start(self):
        if not self.connected:
            self.connected = True
            self.conthr = ConnThread()
            self.conthr.start()

    def sendMessage(self, msg):
        if self.connected:
            s = SendThread(self.sid, 'message', msg)
            s.start()

    def disconnect(self):
        if self.connected:
            self.conthr.setDiscRequest()
            s = SendThread(self.sid, 'disconnect')
            s.start()
            self.connected = False

    def step(self):
        if not self.connected:
            return

        msgs = self.conthr.getMessages()
        for msg in msgs:
            if msg[0] == 'connected':
                self.sid = msg[1]
                if self.hooks['join']:
                    try:
                        self.hooks['join']()
                    except:
                        pass

            elif msg[0] == 'gotMessage':
                if self.hooks['message']:
                    try:
                        self.hooks['message'](msg[1])
                    except:
                        pass

            elif msg[0] == 'strangerDisconnected':
                if self.hooks['leave']:
                    try:
                        self.hooks['leave']()
                    except:
                        pass

            elif msg[0] == 'recaptchaRequired':
                self.sid = msg[1]

                o = OmegleConnection()
                o.setsid(self.sid)
                self.captchaid = o.captchaGetID(msg[2])

                if self.hooks['captchaRequired']:
                    try:
                        self.hooks['captchaRequired']("http://www.google.com/recaptcha/api/image?c=" + self.captchaid)
                    except:
                        pass

            elif msg[0] == 'recaptchaRejected':
                self.disconnect()
                if self.hooks['captchaRejected']:
                    try:
                        self.hooks['captchaRejected']()
                    except:
                        pass

        if self.conthr:
            if not self.conthr.is_alive():
                self.connected = False
        else:
            self.connected = False


    def isConnected(self):
        return self.connected


    def confirmCaptcha(self, code):
        if self.connected:
            s = SendThread(self.sid, 'captcha', self.captchaid, code)
            s.start()
