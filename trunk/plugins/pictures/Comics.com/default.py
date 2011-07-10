##############################################################################
#
# Comics.com - XBMC picture plugin
#
# Version 1.1
# 
# Coding by Dan Dar3 
# http://dandar3.blogspot.com
#
#
# Credits:
#   * Team XBMC @ XBMC.org                                                [http://xbmc.org/]
#   * Leonard Richardson <leonardr@segfault.org>  - BeautifulSoup 3.0.7a  [http://www.crummy.com/software/BeautifulSoup/]
#   * Eric Lawrence      <e_lawrence@hotmail.com> - Fiddler Web Debugger  [http://www.fiddler2.com]
#

# 
# Constants
#
__plugin__  = "Comics.com"
__author__  = "Dan Dar3 <dan.dar33@gmail.com>"
__url__     = "http://dandar3.blogspot.com"
__date__    = "16 January 2010"
__version__ = "1.1"

#
# Imports
#
import os
import sys

LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (LIB_DIR)

#
# Comic strip (list)...
#
if ( "action=list" in sys.argv[ 2 ] ):
    import xbmcplugin_list as plugin
    plugin.Main()
#
# Main...
#
else :
    xbmc.log( "[PLUGIN] %s v%s (%s)" % ( __plugin__, __version__, __date__ ), xbmc.LOGNOTICE )
    import xbmcplugin_main as plugin
    plugin.Main()
