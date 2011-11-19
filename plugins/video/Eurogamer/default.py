##############################################################################
#
# Eurogamer - XBMC video addon
# http://www.eurogamer.net/
#
# Version 1.5
# 
# Coding by Dan Dar3 
# http://dandar3.blogspot.com
#
#
# Credits:
#   * Eurogamer                                                            [http://www.eurogamer.net]
#   * Team XBMC4Xbox                                                       [http://xbmc4xbox.org/]
#   * Leonard Richardson <leonardr@segfault.org>  - BeautifulSoup          [http://www.crummy.com/software/BeautifulSoup/]
#   * Eric Lawrence      <e_lawrence@hotmail.com> - Fiddler Web Debugger   [http://www.fiddler2.com]
#

# 
# Constants
#
__plugin__  = "Eurogamer"
__author__  = "Dan Dar3"
__url__     = "http://dandar3.blogspot.com"
__date__    = "19 November 2011"
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
if ( "action=play" in sys.argv[ 2 ] ):
    import eurogamer_play as plugin
else :
    xbmc.log( "[PLUGIN] %s v%s (%s)" % ( __plugin__, __version__, __date__ ), xbmc.LOGNOTICE )
    import eurogamer_list as plugin

plugin.Main()
