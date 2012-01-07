##############################################################################
#
# Sublight - XBMC video plugin
# http://www.sublight.si/
#
# Version 1.9
# 
# Coding by Dan Dar3 
# http://dandar3.blogspot.com
#
#
# Credits:
#   * Sublight                                                  [http://www.sublight.si/]
#   * Team XBMC4xbox                                            [http://xbmc4xbox.org/]
#

# 
# Constants
#
__plugin__  = "Sublight"
__author__  = "Dan Dar3"
__url__     = "http://dandar3.blogspot.com"
__date__    = "6 January 2012"
__version__ = "1.9"

#
# Imports
#
import os
import sys

LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (LIB_DIR)

#
# Search....
#
if ( "action=search" in sys.argv[ 2 ] ):
    import sublight_search as plugin
    plugin.Main()    
elif ( "action=download" in sys.argv[ 2 ] ):
    import sublight_download as plugin
    plugin.Main()
else:
    import sublight_main as plugin
    plugin.Main()