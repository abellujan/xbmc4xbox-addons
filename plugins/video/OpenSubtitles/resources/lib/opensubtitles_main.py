#
# Imports
#
import os
import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin

#
# Main class
#
class Main:
    def __init__( self ):

        #
        # Search by movie file...
        #
        listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30001), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=search' % ( sys.argv[ 0 ] ), listitem=listitem, isFolder=True)

        #
        # Search for playing movie...
        #
        if xbmc.Player().isPlayingVideo() :
            movie_file = xbmc.Player().getPlayingFile()
            
            listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30002), iconImage="DefaultFolder.png" )
            xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=search&movie_file=%s' % ( sys.argv[ 0 ], urllib.quote_plus( movie_file ) ), listitem=listitem, isFolder=True)

        #
        # Disable sorting...
        #
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
        
        #
        # End of list...
        #
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )