#!/usr/bin/python


filename = "../service-names-port-numbers.xml"
import sys
import re
data = open( filename, 'r' ).read()

find_records = re.compile( r"<record[^>]*>(.*?)</record>", re.DOTALL )


name = re.compile( r"<name>(.*?)</name>", re.DOTALL )
protocol = re.compile( r"<protocol>(.*?)</protocol>", re.DOTALL )
description = re.compile( r"<description>(.*?)</description>", re.DOTALL )
number = re.compile( r"<number>(.*?)</number>", re.DOTALL )
note = re.compile( r"<note>(.*?)</note>", re.DOTALL )
info = {}

for record in find_records.finditer( data ):
	record = record.groups( 1 )[0].replace( "\n", "" ).strip()
	if "<number" in record and "<protocol" in record and "<description>Unass" not in record:
		n = name.search( record )
		
		if n != None:
			
			n = n.group( 1 )
			p = protocol.search( record ).group( 1 ) if protocol.search( record ) != None  else None
			d = description.search( record ).group( 1 ) if description.search( record ) != None else None
			no = note.search( record ).group( 1 ) if note.search( record ) != None else None
			num = number.search( record ).group( 1 ) if number.search( record ) != None else None

			info[ "{}/{}".format( p,num )] = ( n, p, d, no, num )

print info['tcp/80']