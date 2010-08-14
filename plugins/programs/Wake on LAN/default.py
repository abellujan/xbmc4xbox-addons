##############################################################################
#
# Wake on LAN - Program plugin for XBMC
#
# Version 1.0
# 
# Dan Dar3 
# http://dandar3.blogspot.com
#
# Changelog:
#
# v1.0 (Saturday, 14 August 2010):
# - initial release;
#

# 
# Constants
#
__plugin__  = "Wake on LAN"
__author__  = "Dan Dar3 <dan.dar33@gmail.com>"
__url__     = "http://xbmc4xbox-addons.googlecode.com"
__date__    = "14 August 2010"
__version__ = "1.0 beta"


#
# Imports
#
import os
import sys
import urllib
import xbmcgui
import xbmcplugin

LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (LIB_DIR) 

#
# Edit window
#
if ( "action=wake" in sys.argv[ 2 ] ):
    import xbmcplugin_wake as plugin
    plugin.Main()    
#
# Main menu
#
else :
    xbmc.log( "[PLUGIN] %s v%s (%s)" % ( __plugin__, __version__, __date__ ), xbmc.LOGNOTICE )
    import xbmcplugin_main as plugin
    plugin.Main()    
