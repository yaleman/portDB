#!/usr/bin/python


filename = "../service-names-port-numbers.xml"
import os
import sys
import re
data = open( filename, 'r' ).read()

find_records = re.compile( r"<record[^>]*>(.*?)</record>", re.DOTALL )


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

			info[ "{}/{}".format( p,num )] = { 'name' : name, 'protocol' : p, 'description' : d, 'note' : no, 'port' : num }

updated = 0
noupdate = 0
ignored = 0
services = {}
if os.path.exists( "data/" ):
	print "Data directory exists, starting to process."
	for item in info:
		service = info[item]
		servicedir = "data/{}/{}/".format( service['protocol'], service['port'] )
		if os.path.exists( servicedir ): 
			ianafile = servicedir + "/iana.md"
			md = "_Name:_ {}\n\n".format( service['name'] )
			if( service['description'] != None ):
				md += "_Description:_ {}\n\n".format( service['description'] )
			if service['note'] != None:
				md += "_Note:_ {}\n\n".format( service['note'] )
			if servicedir != services:
				services[servicedir] = md
			else:
				print "Duplicate service: {}".format( servicedir )
				print "Original:\n{}".format( services[servicedir] )
				print "New:\n{}".format( md )
			if os.path.exists( ianafile ):
				with open( ianafile, 'r' ) as fh:
					if fh.read() == md:
						noupdate += 1
					else:
						with open( ianafile, 'w' ) as fh:
							fh.write( md )
						updated += 1
			else:
				with open( ianafile, 'w' ) as fh:
					fh.write( md )
				updated += 1
		else:
			ignored += 1
print "Updated: {}/{}".format( updated, ( updated + noupdate ) )
print "Ignored: {}".format( ignored )