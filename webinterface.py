from flask import Flask, render_template, request, url_for

import markdown
import os.path
from math import ceil




def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


def getnotes( proto, port ):
	notes = ""
	filename_notes = "{}notes".format( datadir( proto, port ) )
	if( os.path.exists( filename_notes ) ):
		with open( filename_notes, 'r' ) as fh: 
			notes = markdown.markdown( fh.read().decode( 'utf-8' ) )
	else:
		notes = False
	return notes
	
def datadir( proto, port=None ):
	""" returns the appropriate data directory based on the protocol/port supplied """
	# TODO: include checking for if the directory actually exists.
	if "." in proto :
		abort( 403 )
	if port is None:
		return 'data/{}/'.format( proto.lower() )
	else:
		return  "data/{}/{}/".format( proto.lower(), port )

app = Flask(__name__)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page




@app.route( '/' )
def index():
	""" the site homepage, lists protocols """
	protocols = { 'tcp' : "Transmission Control Protocol", 
				'udp' : "User Datagram Protocol" 
				}
	return render_template( "index.html", protocols=protocols )

@app.route( '/about' )
def about():
	""" return the README.md file in the default template """
	return render_template( "about.html", readme=markdown.markdown( open( 'README.md', 'r' ).read() ) )

@app.route( '/contributing' )
def contributing():
	return render_template( "contributing.html" )

@app.route('/view/<proto>', defaults={'page': 1})
@app.route('/view/<proto>/page/<int:page>')
def viewproto( proto, page ):
	""" view a list of ports associated with this protocol """
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



@app.route('/view/<proto>/<int:port>', methods=['GET'] )
def view( proto, port ):
	ianafile = '{}iana.md'.format( datadir( proto, port ) ) 
	if os.path.exists( ianafile ):
		iana = markdown.markdown( open( ianafile, 'r' ).read() )
	else:
		iana = False
	return render_template( "view.html", proto=proto, port=port, notes=getnotes( proto, port ), iana=iana )


@app.errorhandler(404)
def error404(e):
    return render_template( 'errors/404.html' ), 404
@app.errorhandler(500)
def error500(e):
    return render_template( 'errors/500.html' ), 500




if __name__ == '__main__':
	app.run( debug=True )

