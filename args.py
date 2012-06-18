'''
nick irc(s)://hostname1:port channel1 irc(s)://hostname2:port2 channel2
'''

import argparse

def parseArgs(argv):
	parser = argparse.ArgumentParser(description='Brigde two IRC channels.')
	parser.add_argument('-n', '--nick', metavar='nickname', default='iRcbRg', type=str, nargs='?',
				help='Nickname to appear in both channels. Defaults to "iRcbRg"')
	parser.add_argument('-u', '--user', metavar='username', default='iRcbRg', type=str, nargs='?',
				help='IRC user name. Defaults to "iRcbRg"')
	parser.add_argument('-r', '--real', metavar='real name', default='iRcbRg Smith', type=str, nargs='?',
				help='IRC real name. Defaults to "iRcbRg Smith"')
	parser.add_argument('uri1', metavar='URI_1', type=str,
				help='URI of first IRC server. ex: irc(s)://irc.example.com:1234')
	parser.add_argument('chan1', metavar='channel_1', type=str,
				help='Channel on the first IRC server. ex: (#)python')
	parser.add_argument('uri2', metavar='URI_2', type=str,
				help='URI of second IRC server. ex: irc(s)://irc.example.info:1234')
	parser.add_argument('chan2', metavar='channel_2', type=str,
				help='Channel on the second IRC server. ex: (#)twisted')



	args = parser.parse_args(argv)
	return args

if __name__=='__main__':
	import sys
	print parseArgs(sys.argv)
