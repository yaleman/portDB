""" Web interface and implementation of portDB
see the running version at http://portdb.yaleman.org """

# edit this to show where the app is installed
PROJECT_DIR='/home/portdb/portDB/'
PROTOCOLS = {'tcp' : "Transmission Control Protocol", 'udp' : "User Datagram Protocol"}

# load libs

from os import path, listdir
import sys

# setup the required wsgi/environment stuff
if __name__ != '__main__':
	activate_this = path.join(PROJECT_DIR, 'venv', 'bin', 'activate_this.py')
	execfile(activate_this, dict(__file__=activate_this))
	sys.path.append(PROJECT_DIR)

from flask import request, Flask, url_for, render_template, abort
import markdown
import json

# helper functions


def datadir(proto, port=None):
    """ String datadir( String proto, Int port )
    returns the appropriate data directory based on the protocol/port supplied
    """
    if "." in proto:
        abort(403)
    if port is None:
        protodir = '{}data/{}/'.format(PROJECT_DIR,proto.lower())
        # check if the path actually exists
        if path.exists(protodir):
            return protodir
        else:
            abort(404)
    else:
        linkdir = "{}data/{}/{}/".format(PROJECT_DIR, proto.lower(), port)
        if path.exists(linkdir):
            return linkdir
        else:
            abort(404)


def portlist(proto=None):
	""" returns a list of ports (as strings) based on a proto """
	# TODO: write tests for this, it should be doable.
	if avoidnasty(proto,  None):
		proto = proto.lower()
		ports = [port for port in listdir(datadir(proto)) if port != '.DS_Store']
		return ports


def avoidnasty(proto, port):
	"""
	check against the stored protocols. fairly simple way of avoiding nastiness. terribly broken though.
	"""
	if proto.lower() not in PROTOCOLS:
		abort(404)
        #return False
	if port != None:
		if str( port ) not in listdir('{}/data/{}'.format(PROJECT_DIR, proto)):
			abort(404)
	return True


def url_for_other_page(page):
    """ Provides the URL for another page  based on the function endpoint.
    """
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


# initialize the web app
PORTDB = Flask(__name__)
PORTDB.jinja_env.globals['url_for_other_page'] = url_for_other_page

# web app code 

@PORTDB.route('/')
def index():
	""" the site homepage, lists protocols """
	return render_template("index.html", protocols=PROTOCOLS)


@PORTDB.route('/about')
def about():
  """ return the README.md file in the default template """
  return render_template("about.html", readme=markdown.markdown(open('{}/README.md'.format( PROJECT_DIR ), 'r').read()))


@PORTDB.route('/contributing')
def contributing():
  """ displays the page where people can find out about helping """
  return render_template("contributing.html")


@PORTDB.route('/view/<proto>', defaults={'page': 1})
@PORTDB.route('/view/<proto>/page/<int:page>')
def viewproto(proto, page):
	""" view a list of ports associated with this protocol """
	if avoidnasty(proto, None):
		from pagination import Pagination

		if path.exists(datadir(proto)):
			ports = [port for port in listdir(datadir(proto)) if port != '.DS_Store']
			# count the ports for pagination's sake
			num_ports = len(ports)
			per_page = 500

			if not ports and page != 1:
			# if the list of ports is broken and someone's going to the wrong page, 404 them
				abort(404)
			else:
				# sort them numerically instead of alphabetically.
				ports.sort(key=int)
				if page == 1:
					startpoint = 0
				else:
					startpoint = (page -1) * per_page
				ports = ports[startpoint : (startpoint + per_page)]
				numports = len(ports)

			return render_template("viewproto.html", pagination=Pagination(page, per_page, num_ports), proto=proto, ports=ports, numports=numports, startpoint=startpoint)
		else:
			return index()


@PORTDB.route('/view/<proto>/<int:port>', methods=['GET'])
@PORTDB.route('/view/<proto>/<int:port>/', methods=['GET'])
def view(proto, port):
  """" presents the view of a protocol/port combination """
  proto = proto.lower()
  if avoidnasty(proto, port):
		ianafile = '{}iana.md'.format(datadir(proto, port))
		notesfile = '{}notes.md'.format(datadir(proto, port))
		iana = False
		notes = False
		if path.exists(ianafile):
			iana = markdown.markdown(open(ianafile, 'r').read())
		if path.exists(notesfile):
			with open(notesfile, 'r') as filehandle:
				notes = markdown.markdown(filehandle.read().decode('utf-8'))
		return render_template("view.html", proto=proto, port=port, notes=notes, iana=iana)

def searchports(proto, searchterm):
	""" supply the proto and the searchterm and it'll respond with the list of ports and if there's more than 5 """
	# TODO : write tests for this, it should be doable.
	maxresponses = 10

	ports = [port for port in portlist(proto) if searchterm in port]
	ports.sort(key=int)
	ismore = False
	if len(ports) > maxresponses:
		ismore = True
		ports = ports[:maxresponses]
	return ports, ismore


@PORTDB.route('/api/search/<searchterm>/search.json', methods=['GET'])
def apisearch(searchterm):
  """ this is the start of the API search functionality, still doesn't work """
  data = []
  for proto in PROTOCOLS:
    tmp = [port for port in portlist(proto) if searchterm in port]
    for port in tmp:
      data.append({'proto' : proto, 'port' : port})
  return json.dumps(data)

@PORTDB.route('/api/<proto>/<port>/search.json', methods=['GET'])
@PORTDB.route('/api/<proto>/proto.json', defaults={'port': ""}, methods=['GET'])
def api(proto, port):
  """ returns a json object which should allow searches for things."""
  ports, ismore = searchports(proto, port)
  data = {}
  data['ports'] = list([(proto, port) for port in ports])
  data['ismore'] = ismore
  return json.dumps(data)


@PORTDB.route('/robots.txt')
def robots():
    """ return the robots.txt file """
    return 'User-agent: *\nDisallow:'

@PORTDB.errorhandler(403)
def error403(error):
  """ returns a 403 """
  if error:
    pass
  return render_template('errors/403.html'), 403


@PORTDB.errorhandler(404)
def error404(error):
  """ returns a 404 whenever needed """
  if error:
      pass
  return render_template('errors/404.html'), 404


@PORTDB.errorhandler(500)
def error500(error):
  """ returns a 500 error whenever needed """
  if error:
      pass
  return render_template('errors/500.html'), 500


@PORTDB.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = ' no-cache, no-store'
    return response


if __name__ == '__main__':
	PORTDB.run(debug=True)

else:
	application=PORTDB
#from webinterface  import PORTDB as application
