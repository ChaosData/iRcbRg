#!/usr/bin/python
from args import *
from uri import *
from chan import *
from bot import *

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, ssl
import sys


def validateCLI(cargs):

	uri1 = parseURI(cargs.uri1)
	if(len(uri1)==1):
		print 'invalid URI format for URI_1'
		sys.exit(2)
	
	uri2 = parseURI(cargs.uri2)
	if(len(uri2)==1):
		print 'invalid URI format for URI_2'
		sys.exit(2)
	
	chan1 = parseChan(cargs.chan1)
	if(not chan1[0]):
		print 'illegal characters in channel_1'
		sys.exit(2)

	chan2 = parseChan(cargs.chan2)
	if(not chan2[0]):
		print 'illegal characters in channel_2'
		sys.exit(2)
	
	return uri1, uri2, chan1, chan2


if __name__=='__main__':
        cargs = parseArgs(sys.argv[1:])
	uri1, uri2, chan1, chan2 = validateCLI(cargs)
	botF1 = BridgeBotFactory(cargs.nick, cargs.real, cargs.user, chan1[1])
	botF2 = BridgeBotFactory(cargs.nick, cargs.real, cargs.user, chan2[1])

	#b1 = BridgeBot(cargs.nick, cargs.real, cargs.user, chan1[1])
        #b1.factory = botF1
        #botF1.bot = b1
	
	#b2 = BridgeBot(cargs.nick, cargs.real, cargs.user, chan2[1])
        #b2.factory = botF2
        #botF2.bot = b2                
	
	botF1.otherFactory = botF2
	botF2.otherFactory = botF1

	if(uri1[0]): #ssl
		reactor.connectSSL(uri1[1], uri1[2], botF1, ssl.ClientContextFactory())
	else: #plaintext
		reactor.connectTCP(uri1[1], uri1[2], botF1)

	if(uri2[0]): #ssl
		reactor.connectSSL(uri2[1], uri2[2], botF2, ssl.ClientContextFactory())
	else: #plaintext
		reactor.connectTCP(uri2[1], uri2[2], botF2)

	
	reactor.run()	
