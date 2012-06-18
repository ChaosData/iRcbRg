
def parseURI(URI):
	uri = URI.split('://')
	if(len(uri) == 2):
		uri = [uri[0]] + uri[1].split(':')
		if(len(uri) == 3):
			if( (uri[0] in ['ircs','irc']) and uri[2].isdigit() and int(uri[2])<65535 ):
				return [ [True,False][['ircs','irc'].index(uri[0])], uri[1], int(uri[2]) ]
	return [False]

if __name__=='__main__':
	from args import *
	import sys
	cargs = parseArgs(sys.argv[1:])
	print cargs
	print parseURI(cargs.uri1)
