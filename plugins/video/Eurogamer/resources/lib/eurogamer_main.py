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
        # NOT USED ANYMORE
        #
        return
        
        #
        # Latest videos
        #
        listitem = xbmcgui.ListItem( __language__(30001), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=list&channel=%s&channel_desc=%s' % ( sys.argv[ 0 ], "all",      __language__(30001) ), listitem=listitem, isFolder=True)

        #
        # Trailers
        #
        listitem = xbmcgui.ListItem( __language__(30002), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=list&channel=%s&channel_desc=%s' % ( sys.argv[ 0 ], "trailers", __language__(30002) ), listitem=listitem, isFolder=True)
		
        #
        # Gameplay
        #
        listitem = xbmcgui.ListItem( __language__(30003), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list&channel=%s&channel_desc=%s' % ( sys.argv[ 0 ], "capture", __language__(30003) ), listitem=listitem, isFolder=True)

        #
        # EGVT Show
        #
        listitem = xbmcgui.ListItem( __language__(30004), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list&channel=%s&channel_desc=%s' % ( sys.argv[ 0 ], "show",    __language__(30004) ), listitem=listitem, isFolder=True)

        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
        # End of list...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )