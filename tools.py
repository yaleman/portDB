""" This is the tools library for the portDB project """
import markdown

import os
from flask import Flask, render_template, request, url_for, jsonify, abort


def getnotes( proto, port ):
  """ String getnotes( String proto, Int port )
  returns a markdown-rendered version of a notes file for a given proto/port combination
  returns False if the file doesn't exist.
  """
  filename_notes = "{}notes.md".format( datadir( proto, port ) )
  if( os.path.exists( filename_notes ) ):
    with open( filename_notes, 'r' ) as fh:
      return  markdown.markdown( fh.read().decode( 'utf-8' ) )
  else:
    return False

def url_for_other_page(page):
    """ Documentation to come?
    """
    #TODO: Document this function
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

def datadir( proto, port=None ):
  """ String datadir( String proto, Int port )
  returns the appropriate data directory based on the protocol/port supplied
  """
  # TODO: include checking for if the directory actually exists.
  if "." in proto :
    abort( 403 )
  if port is None:
    return 'data/{}/'.format( proto.lower() )
  else:
    return  "data/{}/{}/".format( proto.lower(), port )

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]
  """ calculate the levenshtein distance between two strings """
