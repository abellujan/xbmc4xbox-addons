#
# Imports
#
from BeautifulSoup      import BeautifulSoup, SoupStrainer
from gametrailers_const import __settings__, __language__, __images_path__
from gametrailers_utils import HTTPCommunicator
import re
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
    #
    # Init
    #
    def __init__( self ) :
        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
        self.plugin_category = params[ "plugin_category" ]
        self.current_page    = int ( params.get( "page", "1" ) ) 

        #
        # Get the videos...
        #
        self.getVideos()
    
    #
    # Get videos...
    #
    def getVideos( self ) :
        # 
        # Get HTML page...
        #
        url           = "http://www.gametrailers.com/feeds/line_listing_results/show_episode_guide/2ea7941b-efc7-45fd-9ade-e5e69ed772fb/?sortBy=most_recent&currentPage=%d" % ( self.current_page )
        htmlData      = HTTPCommunicator().get( url )

        # Parse response...
        beautifulSoup = BeautifulSoup( htmlData )
        
        #
        # Parse movie entries...
        #
        lis = beautifulSoup.findAll ( "div", { "class" : "episode_information" } )
        for li in lis :
            # Thumbnail
            a_thumbnail      = li.find ( "a", { "class" : "thumbnail" } )
            a_thumbnail_imgs = a_thumbnail.findAll ( "img" )
            thumbnail_url    = a_thumbnail_imgs[ -1 ] [ "src" ]

            # Title
            div_description = li.find( "div", { "class" : "description" } )
            h4    = div_description.find ( "h4" )
            title = h4.a.string.strip()
            
            # Video page...
            video_page_url = a_thumbnail[ "href" ]
                
            # Add to list...
            listitem        = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail_url )
            listitem.setInfo( "video", { "Title" : title, "Studio" : "GameTrailers" } )
            plugin_play_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video_page_url ) )
            xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_play_url, listitem=listitem, isFolder=False)     

        # Next page entry...
        listitem = xbmcgui.ListItem (__language__(30503), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(__images_path__, 'next-page.png'))
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = "%s?action=list-retrospectives&plugin_category=%s&page=%i" % ( sys.argv[0], self.plugin_category, self.current_page + 1 ), listitem = listitem, isFolder = True)

        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
        
        # End of directory...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
