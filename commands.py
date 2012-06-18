

def commandHandler(bot, user, channel, command):
	if(command == "names"):
		names(bot, channel)

def names(bot, channel):
	c = 0
	msg = '[Users %s]\n' % (bot.factory.otherFactory.bot.channel)
	for name in bot.factory.otherFactory.bot.known_users:
		msg += "[%s%s]" % (bot.factory.otherFactory.bot.known_users[name]['mode'], name)
		c += 1
		if(c == 5):
			msg += '\n'
			c == 0
		else:
			msg += ' '
	bot.msg(channel, msg)
