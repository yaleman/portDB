from flask import Flask, render_template, request, url_for

import markdown
import os.path
from math import ceil

app = Flask(__name__)


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

@app.route( '/' )
def index():
	""" the site homepage, lists protocols """
	return render_template( "index.html" )

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
	if( os.path.exists ( "data/{}".format( proto.lower() ) ) ):
		ports = [ port for port in os.listdir( "data/{}".format( proto.lower() ) ) if port != '.DS_Store' ]
		# if the list of ports is broken and someone's going to the wrong page, 404 them
		# count the ports for pagination's sake
		num_ports = len( ports )
		per_page = 500

		if not ports and page != 1:
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
				proto=proto.upper(), ports=ports, numports=numports, startpoint=startpoint )
	else:
		return index()

@app.route('/view/<proto>/<int:port>', methods=['GET'] )
def view( proto, port ):
	ianafile = 'data/{}/{}/iana.md'.format( proto, port )
	if os.path.exists( ianafile ):
		iana = markdown.markdown( open( ianafile, 'r' ).read() )
	else:
		iana = False
	return render_template( "view.html", proto=proto.upper(), port=port, notes=getnotes( proto, port ), iana=iana )


@app.errorhandler(404)
def error404(e):
    return render_template( 'errors/404.html' ), 404
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

