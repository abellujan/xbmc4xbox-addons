##############################################################################
#
# Microsoft MIX - XBMC video plugin
# http://http://channel9.msdn.com/events/mix
#
# Version 1.0
# 
# Coding by Dan Dar3 
# http://dandar3.blogspot.com
#
#
# Credits:
#   * Microsoft MIX                                                        [http://www.microsoft.com/events/mix/]
#   * Team XBMC4Xbox @ XBMC4Xbox.org                                       [http://xbmc4xbox.org/]
#   * Leonard Richardson <leonardr@segfault.org>  - BeautifulSoup          [http://www.crummy.com/software/BeautifulSoup/]
#   * Eric Lawrence      <e_lawrence@hotmail.com> - Fiddler Web Debugger   [http://www.fiddler2.com]
#

# 
# Constants
#
__plugin__  = "Microsoft MIX"
__author__  = "Dan Dar3"
__url__     = "http://dandar3.blogspot.com"
__date__    = "2 May 2011"
__version__ = "1.0"

#
# Imports
#
import os
import sys

LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (LIB_DIR)

#
# Sessions (list)
#
if ( "action=sessions" in sys.argv[ 2 ] ):
    import microsoft_mix_sessions as plugin
#
#
#
elif ( "action=play" in sys.argv[ 2 ] ):
    import microsoft_mix_play as plugin
#
# Years (list)
#
else :
    xbmc.log( "[PLUGIN] %s v%s (%s)" % ( __plugin__, __version__, __date__ ), xbmc.LOGNOTICE )
    import microsoft_mix_main as plugin

plugin.Main()
