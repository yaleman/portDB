#!/usr/bin/python


filename = "../service-names-port-numbers.xml"
import os
import sys
import re
data = open( filename, 'r' ).read()

find_records = re.compile( r"<record[^>]*>(.*?)</record>", re.DOTALL )

def writefile( filename, contents ):
	with open( filename, 'w' ) as fh:
		fh.write( contents )

def mkservicedir( service ):
	return "data/{}/{}/".format( service['protocol'], service['port'] )

def ianafilename( service ):
	return "{}iana.md".format( mkservicedir( service ) )

def buildmd( service ):
	md = "_Name:_ {}\n\n".format( service['name'] )
	if( service['description'] != None ):
		md += "_Description:_ {}\n\n".format( service['description'] )
	if service['note'] != None:
		md += "_Note:_ {}\n\n".format( service['note'] )

	return md

re_name = re.compile( r"<name>(.*?)</name>", re.DOTALL )
protocol = re.compile( r"<protocol>(.*?)</protocol>", re.DOTALL )
description = re.compile( r"<description>(.*?)</description>", re.DOTALL )
number = re.compile( r"<number>(.*?)</number>", re.DOTALL )
note = re.compile( r"<note>(.*?)</note>", re.DOTALL )
info = {}

for record in find_records.finditer( data ):
	record = record.groups( 1 )[0].strip()
	# make sure port and protocol are at least defined, ignore unassigned ports
	if "<number" in record and "<protocol" in record and "<description>Unass" not in record.lower():
		name = re_name.search( record )
		
		if name != None:
			
			name = name.group( 1 )
			p = protocol.search( record ).group( 1 ) if protocol.search( record ) != None  else None
			d = description.search( record ).group( 1 ) if description.search( record ) != None else None
			no = note.search( record ).group( 1 ) if note.search( record ) != None else None
			num = number.search( record ).group( 1 ) if number.search( record ) != None else None
			# add the service data to the stored list of services
			info[ "{}/{}".format( p,num )] = { 'name' : name, 'protocol' : p, 'description' : d, 'note' : no, 'port' : num }



updated = 0
noupdate = 0
ignored = 0
services = {}
ignored_services = []
# check you're running from the right directory
if os.path.exists( "data/" ):
	print "Data directory exists, starting to process."
	for item in info:
		# pull the service info
		service = info[item]
		
		if os.path.exists( mkservicedir( service )): 
			# where we'll store the iana info 
			ianafile = ianafilename( service )
			md = buildmd( service )

			if os.path.exists( ianafile ):
				# if the ianafile already exists, check if it's the same as what we're trying to add
				ianafile_contents = open( ianafile, 'r' ).read()
				if ianafile_contents == md:
					noupdate += 1
				# if the data's different, write it out
				else:
					writefile( ianafile, md )
					updated += 1
			else:
				writefile( ianafile, md )
				updated += 1
		else:
			ignored += 1
			if service['protocol'] in ( 'tcp', 'udp' ) and "-" not in service['port']:
				ignored_services.append( { 'protocol' : service['protocol'], 'port' : service['port'], 'name': service['name'], 
						'description' : service['description'], 'note' : service['note'] } )
print "Updated: {}/{}".format( updated, ( updated + noupdate ) )
print "Ignored: {}".format( ignored )

if updated == 0 and len( ignored_services ) > 0:

	while len( ignored_services ) > 0:
		service = ignored_services.pop()
		if not os.path.exists( mkservicedir( service ) ):
				os.makedirs( mkservicedir( service ) )
		writefile( ianafilename( service ), buildmd( service ) )
		print "Added {}".format( mkservicedir( service ) ) 
