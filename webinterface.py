#!/usr/bin/python


import flask
import markdown
import os
import re




app = flask.Flask(__name__)

@app.route( '/' )
def index():
	#html = markdown.markdown(your_text_string)
	retval = ""
	for d in os.listdir( "data/" ):
		retval += "* [{}](/view/{})\n".format( d, d )
		portlist = os.listdir( "data/{}/".format( d ) )
		portlist.sort( key=int )
		for di in portlist:
			retval += "\t* [{}](/view/{}/{})\n".format( di, d, di )
	return flask.render_template( "index.html", content=markdown.markdown( retval ) )

@app.route( '/about' )
def about():
	return flask.render_template( "about.html", readme=markdown.markdown( open( 'README.md', 'r' ).read() ) )

@app.route( '/view/<proto>', methods=['GET'] )
def viewproto( proto ):
	if( os.path.exists ( "data/{}".format( proto ) ) ):
		ports = os.listdir( "data/{}".format( proto ) )
		return flask.render_template( "viewproto.html", proto=proto, ports=ports )
	else:
		return index()

@app.route('/view/<proto>/<int:port>', methods=['GET'] )
def view( proto, port ):
	return flask.render_template( "view.html", proto=proto, port=port, notes=getnotes( proto, port ) )


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

