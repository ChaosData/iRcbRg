
def validChan(chan):
	if( (chan.find('\x07')!=-1) or (chan.find(' ')!=-1) or (chan.find(',')!=-1) or (chan.find(':')!=-1) ):
		return [False]
	if(chan[0] not in ['&','#','+','!']):
		return [True, '#' + chan]
	return [True, chan]	

if __name__=='__main__':
	from args import *
	import sys
	cargs = parseArgs(sys.argv[1:])
	print cargs
	print validChan(cargs.chan1)
