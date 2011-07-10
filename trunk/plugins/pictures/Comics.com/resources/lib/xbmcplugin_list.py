#
# Imports
#
import os
import re
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib
from BeautifulSoup    import SoupStrainer
from BeautifulSoup    import BeautifulSoup
from xbmcplugin_utils import HTTPCommunicator

#
# Main class
#
class Main:
    #
    # Init
    #
    def __init__( self ) :
        # Constants
        self.DEBUG            = False
        self.IMAGES_PATH      = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )
        
        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
        self.comic_name       = urllib.unquote_plus( params[ "comic_name" ] )
        self.comic_url        = urllib.unquote_plus( params[ "comic_url" ] )
        self.current_page     =                int ( params.get( "page", "1" ) )
        
        # Parameters
        if xbmcplugin.getSetting ("entries_per_page") == "0" :
            self.entries_per_page = 5
        elif xbmcplugin.getSetting ("entries_per_page") == "1" :
            self.entries_per_page = 10
        elif xbmcplugin.getSetting ("entries_per_page") == "2" :
            self.entries_per_page = 20

        #
        # Get picture list...
        #
        self.getPictures()
    
    #
    # Get pictures...
    #
    def getPictures( self ) :        
        #
        # Get HTML page...
        #
        httpCommunicator = HTTPCommunicator()
        htmlSource = httpCommunicator.get( "http://comics.com%s?DateAfter=2000-01-01&Order=d.DateStrip+DESC&PerPage=%u&Page=%u" % \
                                           ( self.comic_url, self.entries_per_page, self.current_page ) )

        #
        # Parse HTML page...
        #
        soupStrainer  = SoupStrainer( "div", { "class" : "SRCH_StripList" } )
        beautifulSoup = BeautifulSoup( htmlSource, soupStrainer )
        
        divs_STR_StripFrame = beautifulSoup.findAll( "div", { "class" : "STR_StripFrame" } )
        for div_STR_StripFrame in divs_STR_StripFrame :
            #
            # Title (date)
            #
            div_STR_Day = div_STR_StripFrame.find( "div", { "class" : "STR_Day" } )
            title       = div_STR_Day.string
           
            #
            # Thumbnail & full image...
            #
            div_STR_Comic  = div_STR_StripFrame.find( "div", { "class" : "STR_Comic" } )            
            full_image_url = div_STR_Comic.find( "a", { "class" : "STR_StripImage" } ).img[ "src" ]
            thumbnail_url  = full_image_url.replace( ".full.", ".thumb." )
            
                                    
            # Add directory entry...
            listitem = xbmcgui.ListItem( title, iconImage="DefaultPicture.png", thumbnailImage = thumbnail_url )
            xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url = full_image_url, listitem=listitem, isFolder=False)

        #
        # Next page entry...
        #
        listitem      = xbmcgui.ListItem (xbmc.getLocalizedString(30401), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'next-page.png'))
        next_page_url = "%s?action=list&comic_name=%s&comic_url=%s&page=%u" % ( sys.argv[0], urllib.quote_plus( self.comic_name), urllib.quote_plus( self.comic_url ), self.current_page + 1 )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = next_page_url, listitem = listitem, isFolder = True)
        
        #    
        # Disable sorting...
        #
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
        
        #
        # Label (top-right)...
        #
        xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=( "%s (%s)" % ( self.comic_name, ( xbmc.getLocalizedString(30402) % self.current_page ) ) ) )
        
        #
        # End of directory...
        #
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
