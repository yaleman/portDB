""" Web interface and implementation of portDB
see the running version at http://portdb.yaleman.org """
from flask import Flask, render_template, request, url_for, jsonify, abort


import markdown
import os.path
from math import ceil
from tools import *
import json




# initialize the web app
PORTDB = Flask(__name__)
PORTDB.jinja_env.globals['url_for_other_page'] = url_for_other_page

# going to hard code the protocols
#protocols = [ p.lower() for p in os.listdir( 'data/' ) if p != '.DS_Store' ]
PROTOCOLS = { 'tcp' : "Transmission Control Protocol",
      'udp' : "User Datagram Protocol"
      }


def portlist( proto=None ):
	""" returns a list of ports (as strings) based on a proto """
	# TODO: write tests for this, it should be doable.
	if avoidnasty( proto ):
		proto = proto.lower()
		ports = [ port for port in os.listdir( datadir( proto ) ) if port != '.DS_Store' ]
		return ports


def avoidnasty( proto, port=None ):
	"""
  check against the stored protocols. fairly simple way of avoiding nastiness. terribly broken though.
  """
  #TODO: add valid-port checking
	if proto.lower() not in PROTOCOLS:
		abort( 403 )
		return False
	return True


@PORTDB.route( '/' )
def index():
	""" the site homepage, lists protocols """
	return render_template( "index.html", protocols=PROTOCOLS )


@PORTDB.route( '/about' )
def about():
  """ return the README.md file in the default template """
  return render_template( "about.html", readme=markdown.markdown( open( 'README.md', 'r' ).read() ) )


@PORTDB.route( '/contributing' )
def contributing():
  """ displays the page where people can find out about helping """
  return render_template( "contributing.html" )


@PORTDB.route('/view/<proto>', defaults={'page': 1})
@PORTDB.route('/view/<proto>/page/<int:page>')
def viewproto( proto, page ):
	""" view a list of ports associated with this protocol """
	if avoidnasty( proto ):
		from pagination import Pagination

		if os.path.exists( datadir( proto ) ):
			ports = [ port for port in os.listdir( datadir( proto ) ) if port != '.DS_Store' ]
			# count the ports for pagination's sake
			num_ports = len( ports )
			per_page = 500

			if not ports and page != 1:
			# if the list of ports is broken and someone's going to the wrong page, 404 them
				abort( 404 )
			else:
				# sort them numerically instead of alphabetically.
				ports.sort( key=int )
				if page == 1:
					startpoint = 0
				else:
					startpoint = ( page -1 ) * per_page
				ports = ports[ startpoint : ( startpoint + per_page ) ]
				numports = len( ports )

			return render_template( "viewproto.html", pagination=Pagination( page, per_page, num_ports ),
					proto=proto, ports=ports, numports=numports, startpoint=startpoint )
		else:
			return index()


@PORTDB.route('/view/<proto>/<int:port>', methods=['GET'] )
@PORTDB.route('/view/<proto>/<int:port>/', methods=['GET'] )
def view( proto, port ):
  """" presents the view of a protocol/port combination """
  proto = proto.lower()
  if avoidnasty( proto, port ):
		ianafile = '{}iana.md'.format( datadir( proto, port ) )
		notesfile = '{}notes.md'.format( datadir( proto, port ) )
		iana = False
		notes = False
		if os.path.exists( ianafile ):
			iana = markdown.markdown( open( ianafile, 'r' ).read() )
		if os.path.exists( notesfile ):
			with open( notesfile, 'r' ) as fh:
				notes = markdown.markdown( fh.read().decode( 'utf-8' ) )
		return render_template( "view.html", proto=proto, port=port, notes=notes, iana=iana )

def searchports( proto, searchterm ):
	""" supply the proto and the searchterm and it'll respond with the list of ports and if there's more than 5 """
	# TODO : write tests for this, it should be doable.
	maxresponses = 10

	ports = [ port for port in portlist( proto ) if searchterm in port ]
	ports.sort( key=int )
	ismore = False
	if len( ports ) > maxresponses:
		ismore = True
		ports = ports[:maxresponses]
	return ports, ismore


@PORTDB.route( '/api/search/<searchterm>/search.json', methods=[ 'GET' ] )
def apisearch( searchterm ):
  """ this is the start of the API search functionality, still doesn't work """
  data = []
  for proto in PROTOCOLS:
    tmp = [ port for port in portlist( proto ) if searchterm in port ]
    for port in tmp:
      data.append( { 'proto' : proto, 'port' : port } )
  return json.dumps( data )

@PORTDB.route( '/api/<proto>/<port>/search.json', methods=[ 'GET' ] )
@PORTDB.route( '/api/<proto>/proto.json', defaults={ 'port': "" }, methods=[ 'GET' ] )
def api( proto, port ):
  """ returns a json object which should allow searches for things."""
  ports, ismore = searchports( proto, port )
  data = {}
  data['ports'] = list( [ ( proto, port ) for port in ports ] )
  data['ismore'] = ismore
  return json.dumps( data )


@PORTDB.route('/robots.txt' )
def robots( ):
    """ return the robots.txt file """
    return 'User-agent: *\nDisallow:'

    
@PORTDB.errorhandler(404)
def error404( error ):
  """ returns a 404 whenever needed """
  return render_template( 'errors/404.html' ), 404


@PORTDB.errorhandler(500)
def error500( error ):
  """ returns a 500 error whenever needed """
  return render_template( 'errors/500.html' ), 500


@PORTDB.after_request
def add_header( response ):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = ' no-cache, no-store'
    return response


if __name__ == '__main__':
	PORTDB.run( debug=True )
