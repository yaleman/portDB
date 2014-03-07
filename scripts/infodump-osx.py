#!/usr/bin/python

import subprocess
import re
import os
import pickle

if os.path.exists( 'infodump-osx.pickle' ):
	fh = open( 'infodump-osx.pickle', 'r' )
	infodump = pickle.load( fh )
	fh.close()
else:
	infodump = {}

command = [ "/usr/sbin/lsof", '+c', '0', '-n', '-i', '-P' ]

re_lsof = re.compile( "^(?P<process>[^\s]+)[\s]+[\d]+[\s]+[^\s]+[\s]+[^\s]+[\s]+(?P<ipversion>[^\s]+)[\s]+[\S]+[\s]+[\S]+[\s]+(?P<protocol>[\S]+)[\s](?P<ipstring>[\S]+)[\s]*[\(]*(?P<connectiontype>[^\)]*)[\)]*" )

re_ipv4connect = re.compile( "")
text = subprocess.check_output( command )

for line in [ line for line in text.split( "\n" )[1:] if line.strip() != "" ]:
	data = re_lsof.match( line )
	if data != None:
		process = data.group( 'process' ).replace( '\\x20', " " ) 
		ipstring = data.group( 'ipstring' )
		protocol = data.group( 'protocol' ).lower()
		ipversion = data.group('ipversion' )
		if protocol in [ 'tcp','udp' ]:
			if ipstring != '*:*':
				if data.group( 'connectiontype' ) == "LISTEN":
					port = data.group( 'ipstring' ).split( ":" )[-1]
					server = ( protocol, port, process, ipversion )
					if server not in infodump['servers']:
						servers.append(  server )
						print "New client found: {}".format( server )
				else:
					if ipstring.startswith( "*:" ):
						client = ( process, protocol, ipstring[2:], ipversion )
						if client not in infodump['clients']:
							clients.append( client )
							print "New client found: {}".format( client )
print "Servers: {}".format( infodump['servers'] )
print "Clients: {}".format( infodump['clients'] )



fh = open( 'infodump-osx.pickle', 'wb' )
pickle.dump( infodump, fh )
fh.close()