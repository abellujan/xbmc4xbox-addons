##############################################################################
#
# OpenSubtitles - XBMC "video" plugin
# http://www.opensubtitles.org
#
# Version 1.5
# 
# Coding by Dan Dar3 
# http://dandar3.blogspot.com
#
#
# Credits:
#   * OpenSubtitles.org          [ http://www.opensubtitles.org ]
#   * Team XBMC @ XBMC.org       [ http://xbmc.org ]
#

# 
# Constants
#
__plugin__  = "OpenSubtitles"
__author__  = "Dan Dar3"
__url__     = "http://dandar3.blogspot.com"
__date__    = "6 January 2012"
__version__ = "1.5"

#
# Imports
#
import os
import sys

LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (LIB_DIR)

#
# Main block
#
if ( "action=search" in sys.argv[ 2 ] ):
    import opensubtitles_search   as plugin
elif ( "action=download" in sys.argv[ 2 ] ):
    import opensubtitles_download as plugin
else:
    import opensubtitles_main     as plugin

plugin.Main()
