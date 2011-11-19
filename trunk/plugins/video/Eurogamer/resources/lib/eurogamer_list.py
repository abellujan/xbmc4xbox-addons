#
# Imports
#
from BeautifulSoup import BeautifulStoneSoup, SoupStrainer
from eurogamer_const import __settings__, __language__
from eurogamer_utils import HTTPCommunicator
import os
import re
import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin
import xml.sax.saxutils

#
# Main class
#
class Main:
	#
	# Init
	#
	def __init__( self ) :
		#
		# Constants
		#
		self.IMAGES_PATH  = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )
		self.THUMBNAIL_RE = re.compile( "background-image: url\((.*)\)" ) 
		
		#
		# Parse parameters...
		#
		if sys.argv[ 2 ][ 1: ] != "" :
			params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
		else :
			params = dict()

		#
		# Settings
		#
		self.video_quality    = __settings__.getSetting ("video_quality")

		# Get page...
		self.current_page     = int ( params.get( "page", "1" ) )

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
		url              = "http://www.eurogamer.net/ajax.php?action=frontpage&page=%i" % (self.current_page )
		httpCommunicator = HTTPCommunicator()
		htmlSource       = httpCommunicator.get( url )
				
		#
		# Parse HTML page...
		#
		soupStrainer  = SoupStrainer( "ul" )
		beautifulSoup = BeautifulStoneSoup( htmlSource, parseOnlyThese=soupStrainer )

		# Loop through "playlist" divs...
		uls = beautifulSoup.findAll( "ul", recursive = False )
		for ul in uls:
			lis = ul.findAll( "li", recursive=False )
			for li in lis :
				# Get A link...
				li_a = li.find("a", recursive=False)				
				if (li_a == None) :
					continue
				
				# Video page URL...
				video_page_url = li_a[ "href" ]			
				
				# Thumbnail...
				a_style   = li_a[ "style" ]
				thumbnail = "";
				if (self.THUMBNAIL_RE.match(a_style)) :
					thumbnail = self.THUMBNAIL_RE.search(a_style).group(1) 
				
				# Title
				title = li.div.h2.a.string.strip()
				
				# Plot
				plot = ""
				
				play_script_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video_page_url ) )
	
				# Add directory entry...
				listitem = xbmcgui.ListItem( title, iconImage=thumbnail, thumbnailImage=thumbnail )
				listitem.setInfo( "video", { "Title" : title, "Studio" : "Eurogamer", "Plot" : plot } )
				xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=play_script_url, listitem=listitem, isFolder=False)

		# Next page...
		listitem = xbmcgui.ListItem (__language__(30401), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'next-page.png'))
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = "%s?action=list&page=%i" % ( sys.argv[0], self.current_page + 1 ), listitem = listitem, isFolder = True)
			
		# Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
		# End of directory...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
		
	#
	# Convert HTML to readable strings...
	#
	def html2text ( self, html ):
		return xml.sax.saxutils.unescape( html, { "&#39;" : "'" } )
