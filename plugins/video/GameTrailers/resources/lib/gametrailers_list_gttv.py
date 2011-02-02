#
# Imports
#
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import SoupStrainer

#
# Main class
#
class Main:
    #
    # Init
    #
    def __init__( self ) :
        # Constants
        self.DEBUG         = False
        
        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
        self.plugin_category = params[ "plugin_category" ]

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
        f = urllib2.urlopen("http://www.gametrailers.com/show/gametrailers-tv")
        htmlData = f.read()
        f.close()
        del f
                    
        #
        # Debug
        #
        if (self.DEBUG) :
            f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "page_gttv.html" ), "w")
            f.write( htmlData )
            f.close()

        #
        # Parse HTML response...
        #
        soupStrainer = SoupStrainer("div", { "id" : "trailer_all" } )
        beautifulSoup = BeautifulSoup( htmlData, parseOnlyThese=soupStrainer )

        #
        # Parse past episodes...
        #
        div_trailer_all       = beautifulSoup.find( "div", { "id" : "trailer_all" } )
        div_trailer_all_divs  = div_trailer_all.findAll( "div", recursive=False )
        for div_trailer_all_div in div_trailer_all_divs :
            # Ignore "Splitter" divs...
            if div_trailer_all_div.get("class") == "Splitter" :
                continue
            
            # Video page URL...
            div_movie_title = div_trailer_all_div.find( "div", { "class" : "movie_title" } )
            video_page_url  = div_movie_title.a[ "href" ]
            
            # Title...
            title = div_movie_title.a.renderContents()
            
            # Thumbnail...
            div_gamepage_content_row_thumb = div_trailer_all_div.find( "div", { "class" : "gamepage_content_row_thumb" } )
            thumbnail_url                  = div_gamepage_content_row_thumb.a.img[ "src" ]
            
            # Plot...
            span_MovieDate = div_trailer_all_div.find( "span", { "class" : "MovieDate" } )
            plot           = span_MovieDate.renderContents ().replace("<b>Description:</b> ", "")
            
            # Date...
            span_movie_date = div_trailer_all_div.find( "span", { "class" : "movie_date" } )
            date_display    = span_movie_date.string
                        
            # Add to list...
            listitem        = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail_url )
            listitem.setInfo( "video", { "Title" : title, "Studio" : "GameTrailers", "Plot" : plot, "Genre" : date_display } )
            plugin_play_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video_page_url ) )
            xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_play_url, listitem=listitem, isFolder=False)

        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
        
        # Label (top-right)...
        xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="%s" % self.plugin_category )
        
        # End of directory...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
