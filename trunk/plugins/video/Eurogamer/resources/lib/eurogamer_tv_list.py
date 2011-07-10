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
import xml.sax.saxutils
from BeautifulSoup      import SoupStrainer
from BeautifulSoup      import BeautifulStoneSoup
from eurogamer_tv_utils import HTTPCommunicator

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
		self.channel          = params[ "channel" ] 
		self.channel_desc     = params[ "channel_desc" ]

		# Settings
		self.video_quality    = xbmcplugin.getSetting ("video_quality")

		# Get page...
		self.current_page     = int ( params.get( "page", "0" ) )
		self.entries_per_page = 25

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
		url = "http://www.eurogamer.net/videos/%s/?start=%i" % (self.channel, self.current_page * self.entries_per_page )
		httpCommunicator = HTTPCommunicator()
		htmlSource       = httpCommunicator.get( url )
		
		# Debug
		if (self.DEBUG) :
			print "URL = " + url
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "page_%i.html" % self.current_page), 'w')
			f.write( htmlSource )
			f.close()
		
		#
		# Parse HTML page...
		#
		soupStrainer  = SoupStrainer( "body" )
		beautifulSoup = BeautifulStoneSoup( htmlSource, parseOnlyThese=soupStrainer )
		#beautifulSoup = BeautifulStoneSoup( htmlSource )

		if (self.DEBUG) :
			print "URL = " + url
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "page_%i_a.html" % self.current_page), 'w')
			f.write( str(beautifulSoup) )
			f.close()

		# Loop throuhg "playlist" divs...
		divs_playlist = beautifulSoup.findAll( "div", { "class" : re.compile( "playlist (row0|row1)" ) } )
		for div_playlist in divs_playlist :
			div_screenshot = div_playlist.findNextSibling( "div", { "class" : "screenshot" } )			
			
			# Thumbnail
			icon = div_screenshot.a.img[ "src" ]
			
			#
			div_details = div_screenshot.findNextSibling( "div", { "class" : "details" } )
			
			# Title
			title = self.html2text( div_details.h2.a.string )
			
			# Video URL
			href = "http://www.eurogamer.net/" + div_details.h2.a[ "href" ]
			
			#
			div_meta_details = div_details.findNextSibling( "div", { "class" : "meta-details" } )
						
			# Date
			if div_meta_details.span.b :
				date = div_meta_details.span.b.string.strip()
			else :
				date = div_meta_details.span.string.strip()

			# Plot 
			p    = div_meta_details.findNextSibling( "p" )
			plot = self.html2text( p.string.strip() )
			
			# Play script url...
			if self.video_quality == "1" : # HD
				href += "?size=large"
			play_script_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( href ) )

			# Add directory entry...
			listitem = xbmcgui.ListItem( title, iconImage=icon, thumbnailImage=icon )
			listitem.setInfo( "video", { "Title" : title, "Studio" : "Eurogamer TV", "Plot" : plot, "Genre" : date } )
			xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=play_script_url, listitem=listitem, isFolder=False)

		# Next page...
		listitem = xbmcgui.ListItem (xbmc.getLocalizedString(30401), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'next-page.png'))
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = "%s?action=list&channel=%s&channel_desc=%s&page=%i" % ( sys.argv[0], self.channel, self.channel_desc, self.current_page + 1 ), listitem = listitem, isFolder = True)
			
		# Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
		# Label (top-right)...
		xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=( "%s   (%i - %i)" % ( self.channel_desc, self.current_page * self.entries_per_page + 1, ( self.current_page + 1 ) * self.entries_per_page ) ) )
		
		# End of directory...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
		
	#
	# Convert HTML to readable strings...
	#
	def html2text ( self, html ):
		return xml.sax.saxutils.unescape( html, { "&#39;" : "'" } )
