import flask
import markdown
import os
import re




app = flask.Flask(__name__)

@app.route( '/' )
def index():
	""" the site homepage, lists protocols """
	
	return flask.render_template( "index.html" )

@app.route( '/about' )
def about():
	""" return the README.md file in the default template """
	return flask.render_template( "about.html", readme=markdown.markdown( open( 'README.md', 'r' ).read() ) )

@app.route( '/contributing' )
def contributing():
	return flask.render_template( "contributing.html" )

@app.route( '/view/<proto>', methods=['GET'] )
def viewproto( proto ):
	""" view a list of ports associated with this protocol """
	if( os.path.exists ( "data/{}".format( proto.lower() ) ) ):
		ports = [ port for port in os.listdir( "data/{}".format( proto.lower() ) ) if port != '.DS_Store' ]
		ports.sort( key=int)
		return flask.render_template( "viewproto.html", proto=proto.upper(), ports=ports )
	else:
		return index()

@app.route('/view/<proto>/<int:port>', methods=['GET'] )
def view( proto, port ):
	ianafile = 'data/{}/{}/iana.md'.format( proto, port )
	if os.path.exists( ianafile ):
		iana = markdown.markdown( open( ianafile, 'r' ).read() )
	else:
		iana = False
	return flask.render_template( "view.html", proto=proto.upper(), port=port, notes=getnotes( proto, port ), iana=iana )


@app.errorhandler(404)
def error404(e):
    return flask.render_template( 'errors/404.html' ), 404
@app.errorhandler(500)
def error500(e):
    return render_template( 'errors/500.html' ), 500

def getnotes( proto, port ):
	notes = ""
	filename_notes = "data/{}/{}/notes".format( proto, port ).lower()
	if( os.path.exists( filename_notes ) ):
		with open( filename_notes, 'r' ) as fh: 
			notes = markdown.markdown( fh.read().decode( 'utf-8' ) )
	else:
		notes = False
	return notes
if __name__ == '__main__':
	app.run( debug=True )

