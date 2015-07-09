""" This is the tools library for the portDB project """

from os import path
from flask import request, url_for, abort


def url_for_other_page(page):
    """ Provides the URL for another page  based on the function endpoint.
    """
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

def datadir(proto, port=None):
    """ String datadir( String proto, Int port )
    returns the appropriate data directory based on the protocol/port supplied
    """
    if "." in proto:
        abort(403)
    if port is None:
        protodir = 'data/{}/'.format(proto.lower())
        # check if the path actually exists
        if path.exists(protodir):
            return protodir
        else:
            abort(404)
    else:
        linkdir = "data/{}/{}/".format(proto.lower(), port)
        if path.exists(linkdir):
            return linkdir
        else:
            abort(404)

def levenshtein(string1, string2):
    """ calculate the levenshtein distance between two strings """
    if len(string1) < len(string2):
        return levenshtein(string2, string1)

    # len(string1) >= len(string2)
    if len(string2) == 0:
        return len(string1)

    previous_row = xrange(len(string2) + 1)
    for i, character1 in enumerate(string1):
        current_row = [i + 1]
        for j, character2 in enumerate(string2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than string2
            substitutions = previous_row[j] + (character1 != character2)
            current_row.append(min(insertions, deletions, substitutions))
    previous_row = current_row

    return previous_row[-1]
