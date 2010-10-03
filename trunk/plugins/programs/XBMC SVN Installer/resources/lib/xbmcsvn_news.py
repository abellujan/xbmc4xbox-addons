#
# Imports
#
import sys
import xbmc
import xbmcgui
import xbmcplugin
import traceback
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup
from xbmcsvn_utils import HTTPCommunicator
from xbmcsvn_utils import HTMLStripper

#
# Main class
#
class GUI( xbmcgui.WindowXMLDialog ):
    ACTION_EXIT_SCRIPT = ( 9, 10, 216, 257, 61448, )

    #
    #
    #
    def __init__( self, *args, **kwargs ):
        # Show dialog window...
        self.doModal()

    #
    #
    #
    def onInit( self ):
        #
        # Init
        #
        
        #
        # Wait...
        #        
        dialogProgress = xbmcgui.DialogProgress()
        dialogProgress.create( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30200) )

        try :            
            #
            # Get the news...
            #
            httpCommunicator = HTTPCommunicator()
            htmlData         = httpCommunicator.get( "http://www.sshcs.com/xbmc/")
    
            #
            # Parse the HTML...
            #
            output_text      = "\n"
            soupStrainer     = SoupStrainer( "div", { "class" : "welcomenews" } )
            beautifulSoup    = BeautifulSoup( htmlData, parseOnlyThese=soupStrainer)

            div_welcomenews      = beautifulSoup.find( "div", { "class" : "welcomenews" });
            div_welcomenews_divs = div_welcomenews.findAll( "div" );
            
            # Title
            divs              = div_welcomenews_divs[ 1 ].findAll( "div")
            build             = divs [ 1 ].string.strip()
            uploaded          = divs [ 2 ].string.replace("Uploaded", "").strip()
            output_text       = output_text + "%s   [%s]\n\n" % ( build, uploaded )
            
            # Text
            htmlStripper      = HTMLStripper()
            htmlStripper.feed( str( div_welcomenews_divs[0] ).replace( "<br />", "\n" ).replace("<p>", "\n<p>") )
            output_text       = output_text + htmlStripper.get_fed_data()
            
        #
        # Aw :(
        #
        except Exception :
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            output_text = repr(traceback.format_exception(exceptionType, exceptionValue, exceptionTraceback))
        
        #
        # Output text...
        #
        self.getControl( 5 ).setText( output_text )
        
        #
        # Close progress dialog...
        #
        dialogProgress.close()

    #
    # onClick handler
    #
    def onClick( self, controlId ):
        pass

    #
    # onFocus handler
    #
    def onFocus( self, controlId ):
        pass

    #
    # onAction handler
    #
    def onAction( self, action ):
        if action and ( action in self.ACTION_EXIT_SCRIPT ):
            self.close()            
