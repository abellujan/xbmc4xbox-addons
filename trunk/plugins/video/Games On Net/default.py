##############################################################################
#
# Games On Net - XBMC video plugin
# http://games.on.net
#
# Version 1.0
# 
# Coding by Dan Dar3 
# http://dandar3.blogspot.com
#
#
# Credits:
#   * Games On Net                                                       [ http://games.on.net ]
#   * Team XBMC4Xbox                                                     [ http://xbmc4xbox.org/ ]
#   * Leonard Richardson <leonardr@segfault.org> - BeautifulSoup         [ http://www.crummy.com/software/BeautifulSoup/ ]
#   * Eric Lawrence <e_lawrence@hotmail.com>     - Fiddler Web Debugger  [ http://www.fiddler2.com ]
#

# 
# Constants
#
__plugin__  = "Games On Net"
__author__  = "Dan Dar3"
__url__     = "http://dandar3.blogspot.com"
__date__    = "6 July 2009"
__version__ = "1.0"

#
# Imports
#
import os
import sys

LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (LIB_DIR)

#
# Play
#
if ( "action=play" in sys.argv[ 2 ] ):
    import gamesonnet_play as plugin
#
# Main menu
#
else :
    import gamesonnet_list as plugin

plugin.Main()
