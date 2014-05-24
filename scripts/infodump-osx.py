#!/usr/bin/python

import subprocess
import re
import os
import sys
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

re_ipstring = "(?P<ip>[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})"
re_ips = re.compile( "inet {}".format( re_ipstring ) )
re_server = re.compile( "({}|\*):(?P<port>[\d]+)".format( re_ipstring ) )
ifconfig = subprocess.check_output( "/sbin/ifconfig" )
ips = re_ips.findall( ifconfig )



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
						infodump['servers'].append(  server )
						print "New client found: {}".format( server )
				else:
					if re_server.match( ipstring ) != None:
						print ipstring
						client = ( process, protocol, ipstring[2:], ipversion )
						if client not in infodump['clients']:
							infodump['clients'].append( client )
							print "New client found: {}".format( client )
					else:
						#print ipstring
						src, dest = ipstring.split( r'->' )
						#rint src, dest
#print "Servers: {}".format( infodump['servers'] )
#print "Clients: {}".format( infodump['clients'] )



fh = open( 'infodump-osx.pickle', 'wb' )
pickle.dump( infodump, fh )
fh.close()