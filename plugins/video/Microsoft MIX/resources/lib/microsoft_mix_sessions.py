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
# Constants
# 
__settings__ = xbmcplugin
__language__ = xbmc.getLocalizedString

#
# Main class
#
class Main:
    #
    # Init
    #
    def __init__( self ) :
        # Constants
        self.IMAGES_PATH  = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )
        
        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
        self.sessions_url = urllib.unquote_plus( params.get( "sessions_url" ) ) 
        
        #
        # Get sessions...
        #
        self.getSessions()
        
    #
    # Get years...
    #
    def getSessions(self):
        # 
        # Get HTML...
        #         
        httpCommunicator = HTTPCommunicator()
        url              = "http://channel9.msdn.com%s" % ( self.sessions_url )
        htmlData         = httpCommunicator.get( url )
        
        #
        # Get sessions...
        #
        soupStrainer  = SoupStrainer( "div", { "class" : "tab-content" } )
        beautifulSoup = BeautifulSoup( htmlData, soupStrainer, convertEntities=BeautifulSoup.HTML_ENTITIES )
        
        ul_entries    = beautifulSoup.find( "ul", { "class" : "entries sessions sessionList" } )
        li_entries    = ul_entries.findAll( "li", recursive=False)
        for li_entry in li_entries :
            # Thumbnail...
            div_entry_image = li_entry.find( "div", { "class" : "entry-image" } )
            thumbnail       = div_entry_image.img[ "src" ]
            
            # Meta...
            div_entry_meta  = li_entry.find( "div", { "class" : "entry-meta" } )
            session_url     = div_entry_meta.a[ "href" ]
            session_title   = div_entry_meta.a.string
            
            # Meta - Details
            ul_details      = div_entry_meta.find( "ul", { "class" : "details" } )
            li_speakers     = ul_details.find( "li", { "class" : "grouping speaker"} )
            
            # Speakers...
            speakers        = None
            if (li_speakers != None) :
                speakers    = "".join( [ s.string for s in li_speakers.contents ] ).replace( "\n", " " ).strip()
            
            # Tags..
            li_tags         = ul_details.find( "li", { "class" : "grouping track"} )
            tags            = None
            if (li_tags     != None) :
                tags        = "".join( [ s.string for s in li_tags.contents ] ).replace( "\n", " " ).strip()
            
            # Description...
            div_description = div_entry_meta.find( "div", { "class" : "description" } )
            plot            = div_description.string.strip()
            
            # Title...
            title           = "%s" % ( session_title )
            
            # Add to list...
            listitem        = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
            listitem.setInfo( "video", { "Title" : title, "Studio" : "Microsoft MIX", "Director" : speakers, "PlotOutline" : tags, "Plot" : plot } )
            plugin_url      = '%s?action=play&session_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( session_url ) )
            xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_url, listitem=listitem, isFolder=False, totalItems=10)            
        
        #
        # Next page...
        #
        ul_paging      = beautifulSoup.find( "ul", { "class" : "paging" } )
        li_entries     = ul_paging.findAll( "li", recursive=False)
        sessions_url   = None
        select_next    = False
        for li_entry in li_entries :
            if (select_next) :
                sessions_url = li_entry.a[ "href" ]
                break
            
            if (li_entry.span != None and li_entry.span["class"] == "current") :
                select_next = True
                continue
        
        # Next page entry...
        if (sessions_url != None) :
            listitem = xbmcgui.ListItem (__language__(30401), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'next-page.png'))
            xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = "%s?action=sessions&sessions_url=%s" % ( sys.argv[0], urllib.quote_plus( sessions_url ) ), listitem = listitem, isFolder = True)
                    
        # End of directory...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
