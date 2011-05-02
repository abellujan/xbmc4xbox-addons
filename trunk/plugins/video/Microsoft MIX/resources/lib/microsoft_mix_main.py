#
# Imports
#
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib
from BeautifulSoup       import SoupStrainer
from BeautifulSoup       import BeautifulSoup
from microsoft_mix_utils import HTTPCommunicator

#
# Main class
#
class Main:
    #
    # Init
    #
    def __init__( self ) :
        #
        # Get years...
        #
        self.getYears()
        
    #
    # Get years...
    #
    def getYears(self):
        # 
        # Get HTML...
        #         
        httpCommunicator = HTTPCommunicator()
        url              = "http://channel9.msdn.com/events/mix"
        htmlData         = httpCommunicator.get( url )
        
        #
        # Parse HTML...
        #
        soupStrainer  = SoupStrainer( "div", { "class" : "area-content" } )
        beautifulSoup = BeautifulSoup( htmlData, soupStrainer )
        
        ul_entries    = beautifulSoup.find( "ul", { "class" : "entries recentEvents" } )
        li_entries    = ul_entries.findAll( "li" )
        for li_entry in li_entries :
            # Thumbnail...
            div_entry_image = li_entry.find( "div", { "class" : "entry-image" } )
            thumbnail       = div_entry_image.img[ "src" ]
            
            # Meta...
            div_entry_meta  = li_entry.find( "div", { "class" : "entry-meta" } )
            sessions_url    = div_entry_meta.a[ "href" ]
            sessions_title  = div_entry_meta.a.string
            
            div_data        = div_entry_meta.find( "div", { "class" : "data" } )
            sessions_date   = div_data.find( "span", { "class" : "date" } ).string.replace( "\r\n", "" ).replace( "\t", " " ).replace( "  ", " ")
            sessions_count  = div_data.find( "span", { "class" : "sessionCount" } ).string
            
            # Title...
            title           = "%s (%s)" % ( sessions_title, sessions_date )
            
            # Add to list...
            listitem        = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
            listitem.setInfo( "video", { "Title" : title, "Studio" : "Microsoft MIX" } )
            plugin_url      = '%s?action=sessions&sessions_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( sessions_url ) )
            xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_url, listitem=listitem, isFolder=True)            
            
        # End of directory...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
