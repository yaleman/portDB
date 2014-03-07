#!/usr/bin/python

import subprocess
import re

command = [ "/usr/sbin/lsof", '+c', '0', '-n', '-i', '-P' ]
# | /usr/bin/awk '{ print $1 \" \" $5  \" \" $8 \" \" $9 \" \" $10}'"
re_lsof = re.compile( "^(?P<process>[^\s]+)[\s]+[\d]+[\s]+[^\s]+[\s]+[^\s]+[\s]+(?P<ipversion>[^\s]+)[\s]+[\S]+[\s]+[\S]+[\s]+(?P<protocol>[\S]+)[\s](?P<ipstring>[\S]+)[\s]*[\(]*(?P<connectiontype>[^\)]*)[\)]*" )

re_ipv4connect = re.compile( "")
text = subprocess.check_output( command )
for line in [ line for line in text.split( "\n" )[1:] if line.strip() != "" ]:
	data = re_lsof.match( line )
	if data != None:
		if data.group( 'protocol' ) in [ 'TCP','UDP' ]:
			if data.group('ipstring' ) != '*:*':
				print data.group( 'protocol' ), data.group( 'ipstring' ), data.group( 'connectiontype' )
