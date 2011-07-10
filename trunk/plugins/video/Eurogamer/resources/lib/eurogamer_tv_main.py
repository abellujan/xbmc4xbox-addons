#
# Imports
#
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin

#
# Main class
#
class Main:
    def __init__( self ):
        #
        # Latest videos
        #
        listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30001), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=list&channel=%s&channel_desc=%s' % ( sys.argv[ 0 ], "all",      xbmc.getLocalizedString(30001) ), listitem=listitem, isFolder=True)

        #
        # Trailers
        #
        listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30002), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=list&channel=%s&channel_desc=%s' % ( sys.argv[ 0 ], "trailers", xbmc.getLocalizedString(30002) ), listitem=listitem, isFolder=True)
		
        #
        # Gameplay
        #
        listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30003), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list&channel=%s&channel_desc=%s' % ( sys.argv[ 0 ], "capture", xbmc.getLocalizedString(30003) ), listitem=listitem, isFolder=True)

        #
        # EGVT Show
        #
        listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30004), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list&channel=%s&channel_desc=%s' % ( sys.argv[ 0 ], "show",    xbmc.getLocalizedString(30004) ), listitem=listitem, isFolder=True)

        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
        # End of list...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )