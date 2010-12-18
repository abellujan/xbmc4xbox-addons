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
        soupStrainer = SoupStrainer("div", { "class" : "gttv_main_column" } )
        beautifulSoup = BeautifulSoup( htmlData, parseOnlyThese=soupStrainer )
        
        #
        # Parse current episode...
        #
        div_gttv_top_section  = beautifulSoup.find( "div", { "class" : "gttv_top_section" } )
        div_gttv_episode_part = div_gttv_top_section.find( "div", { "class" : "gttv_episode_part" } )

        # Video page URL...
        div_gttv_episode_part_image = div_gttv_episode_part.find( "div", { "class" : "gttv_episode_part_image" } )
        video_page_url              = div_gttv_episode_part_image.a[ "href" ]
        
        # Thumbnail...
        thumbnail_url = "http://www.gametrailers.com%s" % div_gttv_episode_part_image.a.img[ "src" ]
        
        # Title...
        div_gttv_episode_part_title = div_gttv_episode_part.find( "div", { "class" : "gttv_episode_part_title gttv_title" } )
        title                       = div_gttv_episode_part_title.a.string.strip() 
        
        # Add to list...
        listitem        = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail_url )
        listitem.setInfo( "video", { "Title" : title, "Studio" : "GameTrailers" } )
        plugin_play_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video_page_url ) )
        xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_play_url, listitem=listitem, isFolder=False)        
        
        #
        # Parse past episodes...
        #
        div_gttv_bottom_section = beautifulSoup.find( "div", { "class" : "gttv_bottom_section" } )
        divs_gttv_past_episode  = div_gttv_bottom_section.findAll( "div", { "class" : "gttv_past_episode" } )
        for div_gttv_past_episode in divs_gttv_past_episode :
            # Video page URL...
            div_gttv_past_episode_image = div_gttv_past_episode.find( "div", { "class" : "gttv_past_episode_image" } )
            video_page_url              = div_gttv_past_episode_image.a[ "href" ]
            
            # Thumbnail...
            thumbnail_url = div_gttv_past_episode_image.a.img[ "src" ]
            
            # Date...
            div_gttv_past_episode_title = div_gttv_past_episode.find( "div", { "class" : "gttv_past_episode_title gttv_title" } )
            date_display                = div_gttv_past_episode_title.contents[ 2 ].strip()
            
            # Title...
            div_gttv_past_episode_description = div_gttv_past_episode.find( "div", { "class" : "gttv_past_episode_description gttv_text" } )
            title                             = div_gttv_past_episode_description.string.strip() 
            
            # Add to list...
            listitem        = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail_url )
            listitem.setInfo( "video", { "Title" : title, "Studio" : "GameTrailers", "Genre" : date_display } )
            plugin_play_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video_page_url ) )
            xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_play_url, listitem=listitem, isFolder=False)

        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
        
        # Label (top-right)...
        xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="%s" % self.plugin_category )
        
        # End of directory...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
