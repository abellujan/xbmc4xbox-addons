#
# Imports
#
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib

#
# Main class
#
class Main:
    def __init__( self ):
        # Constants
        IMAGES_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )        
        
        #
        # Search...
        #
        listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30009), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=list-search&query=&plugin_category=%s' % ( sys.argv[ 0 ], xbmc.getLocalizedString(30008) ), listitem=listitem, isFolder=True)
		
        #
        # Previous search queries...
        #
        try :
            saved_queries = eval( xbmcplugin.getSetting( "saved_queries" ) )
        except :
            saved_queries = []
        
        for query in saved_queries :
            listitem = xbmcgui.ListItem( query, iconImage="DefaultFolder.png" )
            xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), 
                                        url = '%s?action=list-search&query=%s&plugin_category=%s' % ( sys.argv[ 0 ], urllib.quote( query ), xbmc.getLocalizedString(30008) ), 
                                        listitem=listitem, 
                                        isFolder=True)		

        # Label (top-right)...
        xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=( "%s" % xbmc.getLocalizedString(30008) ) )

        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
        # End of list...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )