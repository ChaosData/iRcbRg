iRcbRg:
======

### An IRC to IRC bridge, 'nuff said. ###


************************
iRcbRg (irk-berg) is used to relay messages between two IRC channels on two different servers.
************************

How to use it
-------------
```
python iRcbRg.py "irc://irc.freenode.net:6667" "#python" "ircs://irc.example.com:6697" "#python"
```
Don't forget to read the help.
```
$ ./iRcbRg.py -h
usage: iRcbRg.py [-h] [-n [nickname]] [-u [username]] [-r [real name]]
                 URI_1 channel_1 URI_2 channel_2

Brigde two IRC channels.

positional arguments:
  URI_1                 URI of first IRC server. ex:
                        irc(s)://irc.example.com:1234
  channel_1             Channel on the first IRC server. ex: (#)python
  URI_2                 URI of second IRC server. ex:
                        irc(s)://irc.example.info:1234
  channel_2             Channel on the second IRC server. ex: (#)twisted

optional arguments:
  -h, --help            show this help message and exit
  -n [nickname], --nick [nickname]
                        Nickname to appear in both channels. Defaults to
                        "iRcbRg"
  -u [username], --user [username]
                        IRC user name. Defaults to "iRcbRg"
  -r [real name], --real [real name]
                        IRC real name. Defaults to "iRcbRg Smith"
```

Dependencies
------------
Python 2.7 - it uses [argparse](http://docs.python.org/dev/library/argparse.html)
Twisted/Twisted-Words - On Ubuntu 12.04: sudo apt-get install python-twisted-words
