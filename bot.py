from commands import commandHandler

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, ssl


import time, sys


class BridgeBot(irc.IRCClient):
	
	def __init__(self, nick, real, user, channel):
		self.nickname = nick
		self.realname = real
		self.username = user
		self.channel = channel
		self.known_users = dict({})

	##### Connections
	
	def connectionMade(self):
		irc.IRCClient.connectionMade(self)
		print "[connected at %s]" % time.asctime(time.localtime(time.time()))

	def connectionLost(self, reason):
		irc.IRCClient.connectionLost(self, reason)
		print "[disconnected at %s]" % time.asctime(time.localtime(time.time()))

	##### Custom

	def who(self, channel):
		self.sendLine('WHO %s' % channel)

	def updateUsers(self, user):
		self.known_users[user[5]] = dict({'name':user[5], 'mode':(user[6][-1] if(len(user[6])>1) else ' ')})
	
	def updateUser(self, user):
		mode = ' '
		for chan in user[2].split(' '):
			if(len(self.channel)+2 == len(chan)):
				if(self.channel == chan[2:]):
					mode = chan[0]
					break;
		self.known_users[user[1]] = dict({'name':user[1], 'mode':mode})


	##### Regular Methods
		
	def privmsg(self, user, channel, msg):
		user = user.split('!')[0]
		
		#pm
		if channel == self.nickname:
			return

		#bot actions
		if(msg.startswith(self.nickname + ": ")):
			commandHandler(self, user, channel, msg[len(self.nickname + ": "):])
			return
		
		self.factory.otherFactory.bot.msg(self.factory.otherFactory.bot.channel,
							"<%s%s> %s" % (self.known_users[user]['mode'],user, msg))	
	

	def joined(self, channel):
		self.who(channel)


	def modeChanged(self, user, channel, set, modes, args):
		if(channel != self.nickname):
			sign = ('+' if(set) else '-')
			argl = []
			for arg in args:
				if(arg != None):
					argl.append(' ' + str(arg))
							
			self.factory.otherFactory.bot.msg(self.factory.otherFactory.bot.channel,
								"-!- mode/%s [%s%s%s] by %s" % (channel, sign, modes,
												''.join(argl), user.split('!')[0]) )

	
	def signedOn(self):
		self.join(self.channel)


	def userKicked(self, kickee, channel, kicker, message):
		self.factory.otherFactory.bot.msg(self.factory.otherFactory.bot.channel,
							"-!- %s was kicked from %s by %s [%s]" % (kickee,channel,kicker,message))

	def action(self, user, channel, msg):
		self.factory.otherFactory.bot.msg(self.factory.otherFactory.bot.channel,
							"* %s %s" % (user.split('!')[0], msg))
	
	def topicUpdated(self, user, channel, newTopic):
		if(user == self.hostname):
			return
		self.factory.otherFactory.bot.msg(self.factory.otherFactory.bot.channel,
							"-!- %s changed the topic of %s to: %s" % (user,channel,newTopic))
	
	def alterCollidedNick(self, nickname):
		return nickname + '^'


	#### IRC Protocol Methods
	def irc_JOIN(self, prefix, params):
		user = prefix.split('!')		
		if(user[0] == self.nickname):
			self.joined(params[0])
			return;
		self.whois(user[0])
		self.factory.otherFactory.bot.msg(self.factory.otherFactory.bot.channel,
							"-!- %s [%s] has joined %s" % (user[0],user[1], params[0]))

	def irc_PART(self, prefix, params):
		user = prefix.split('!')
		p2=''
		if(len(params)==2):
			p2 = params[1]
		self.factory.otherFactory.bot.msg(self.factory.otherFactory.bot.channel,
							"-!- %s [%s] has left %s [%s]" % (user[0],user[1], params[0],p2))

	def irc_QUIT(self, prefix, params):
		user = prefix.split('!')
		self.factory.otherFactory.bot.msg(self.factory.otherFactory.bot.channel,
							"-!- %s [%s] has quit [%s]" % (user[0],user[1], params[0]))

	def irc_NICK(self, prefix, params):
		self.factory.otherFactory.bot.msg(self.factory.otherFactory.bot.channel,
							"-!- %s is now know as %s" % (prefix.split('!')[0], params[0]))
	def irc_ERR_NOSUCHCHANNEL(self, *nargs):
		print "Connection Failed: channel '%s' is illegal on %s" % (self.channel, self.hostname)
		reactor.stop()

	def irc_RPL_WHOREPLY(self, serv, user):
		self.updateUsers(user)

	def irc_RPL_WHOISCHANNELS(self, server, user):
		self.updateUser(user)
	
	#def irc_unknown(self, prefix, command, params):


class BridgeBotFactory(protocol.ClientFactory):

	def __init__(self, nick, real, user, channel):
		self.nickname = nick
		self.realname = real
		self.username = user
		self.channel = channel
		self.bot = None
		self.otherFactory = None

	def buildProtocol(self, addr):
		b = BridgeBot(self.nickname, self.realname, self.username, self.channel)
		b.factory = self
		self.bot = b
		return b

	def clientConnectionLost(self, connector, reason):
		connector.connect()

	def clientConnectionFailed(self, connector, reason):
		print "Connection Failed:", reason
		reactor.stop()


if __name__ == '__main__':

	nick = 'twistedguyonirc'
	real = 'twisted'
	user = 'twisted'
	chan1 = '#chaosdata'
	chan2 = '#anime'
	server1 = 'irc.freenode.net'
	server2 = 'isis.poly.edu'
	port1 = 6697
	port2 = 6697

	botfac1 = BridgeBotFactory(nick,real,user, chan1)
	botfac2 = BridgeBotFactory(nick,real,user, chan2)

	botfac1.otherFactory = botfac2
	botfac2.otherFactory = botfac1

	reactor.connectSSL(server1, port1, botfac1, ssl.ClientContextFactory())
	reactor.connectSSL(server2, port2, botfac2, ssl.ClientContextFactory())

	reactor.run()
