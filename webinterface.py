#!/usr/bin/python


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

@app.route( '/view/<proto>', methods=['GET'] )
def viewproto( proto ):
	""" view a list of ports associated with this protocol """
	if( os.path.exists ( "data/{}".format( proto.lower() ) ) ):
		ports = os.listdir( "data/{}".format( proto.lower() ) )
		ports.sort( key=int)
		return flask.render_template( "viewproto.html", proto=proto.upper(), ports=ports )
	else:
		return index()

@app.route('/view/<proto>/<int:port>', methods=['GET'] )
def view( proto, port ):
	return flask.render_template( "view.html", proto=proto.upper(), port=port, notes=getnotes( proto, port ) )


def getnotes( proto, port ):
	notes = ""
	filename_notes = "data/{}/{}/notes".format( proto, port )
	if( os.path.exists( filename_notes ) ):
		notes = markdown.markdown( open( filename_notes, 'r' ).read().decode("utf-8") )
	else:
		notes = "{} doesn't exist".format( filename_notes )	
	return notes
if __name__ == '__main__':
	app.run( debug=True )

