#
# Imports
#
import os
import re
import sys
import xbmc
import xbmcgui
import xbmcplugin
import simplejson
import urllib
from urlparse import urlparse
from xml.dom  import minidom
from gamespot_videos_utils import HTTPCommunicator

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
		#
		# Constants
		#
		self.VIDEO_PAGE_URL2 = re.compile( ".*/video/(\d+)/.*" )
		self.VIDEO_PAGE_URL3 = re.compile( ".*/video[s]?/.*-(\d+)" )
		
		#
		# Parse parameters...
		#
		params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
		
		self.video_page_url = urllib.unquote( params[ "video_page_url" ] )
		self.play_hd        = urllib.unquote( params[ "play_hd" ] ) 

		# Settings
		self.video_players = { "0" : xbmc.PLAYER_CORE_AUTO,
							   "1" : xbmc.PLAYER_CORE_DVDPLAYER,
							   "2" : xbmc.PLAYER_CORE_MPLAYER }
		self.video_player = xbmcplugin.getSetting ("video_player")
		
		#
		# Get current item details...
		#
		self.video_title     = unicode( xbmc.getInfoLabel( "ListItem.Title"  ), "utf-8" )
		self.video_thumbnail =          xbmc.getInfoImage( "ListItem.Thumb"  )
		self.video_studio    = unicode( xbmc.getInfoLabel( "ListItem.Studio" ), "utf-8" )
		self.video_plot      = unicode( xbmc.getInfoLabel( "ListItem.Plot"   ), "utf-8" )
		self.video_genre     = unicode( xbmc.getInfoLabel( "ListItem.Genre"  ), "utf-8" )

		#
		# Play video...
		#
		self.playVideo()
	
	#
	# Play video...
	#
	def playVideo( self ) :
		#
		# Show wait dialog while parsing data...
		#
		dialogWait = xbmcgui.DialogProgress()
		dialogWait.create( __language__(30403), self.video_title )
		
		# 
		# Case 1: The id is part of the query (id=xyz) 
		# e.g. http://www.gamespot.com/xbox360/action/wanted/video_player.html?id=cSEynjOr5bIIvzTZ
		#
		if ("?id=" in self.video_page_url) :
			parsed    = urlparse(self.video_page_url)
			params    = dict(part.split('=') for part in parsed[4].split('&'))
			video_id  = params[ "id" ]
			video_url = "http://userimage.gamespot.com/cgi/deliver_user_video.php?id=%s" % ( video_id )
		#
		# Case 2: The id is part of the query (?sid=xyz)
		# e.g. http://uk.gamespot.com/events/gamescom-2012/video.html?sid=6392231
		#
		elif ("?sid=" in self.video_page_url) :
			parsed    = urlparse(self.video_page_url)
			params    = dict(part.split('=') for part in parsed[4].split('&'))
			video_id  = params[ "sid" ]
			
			if video_id != None :
				#
				# Call xml.php to get the address to the .FLV movie...
				#
				httpCommunicator = HTTPCommunicator()
				xml_php_url = "http://www.gamespot.com/pages/video_player/xml.php?id=%s" % str( video_id )
				xmlData     = httpCommunicator.get( xml_php_url )
				
				# Add the xml declaration + character encoding (missing)...
				xmlData = "<?xml version=\"1.0\" encoding=\"iso8859-1\" ?>" + os.linesep + xmlData

				# Parse the response...
				xmldoc      = minidom.parseString( xmlData )

				# Get the HTTP url...
				playlistNode = xmldoc.documentElement.getElementsByTagName( "playList" )[0]
				clipNode     = playlistNode.getElementsByTagName( "clip" )[0]
				uriNode      = clipNode.getElementsByTagName( "URI" )[0]
				
				# SD or HD...
				video_url = uriNode.childNodes[0].nodeValue
				
				# cleanup
				xmldoc.unlink()
		#
		# Other
		#
		else :
			video_id = None
			
			if (self.VIDEO_PAGE_URL2.match( self.video_page_url )) :
				video_id = self.VIDEO_PAGE_URL2.search( self.video_page_url ).group(1)
			if (self.VIDEO_PAGE_URL3.match( self.video_page_url )) :
				video_id = self.VIDEO_PAGE_URL3.search( self.video_page_url ).group(1)
			
			if video_id != None :
				#
				# Call xml.php to get the address to the .FLV movie...
				#
				httpCommunicator = HTTPCommunicator()
				xml_php_url = "http://www.gamespot.com/pages/video_player/xml.php?id=%s" % str( video_id )
				xmlData     = httpCommunicator.get( xml_php_url )
				
				# Add the xml declaration + character encoding (missing)...
				xmlData = "<?xml version=\"1.0\" encoding=\"iso8859-1\" ?>" + os.linesep + xmlData

				# Parse the response...
				xmldoc      = minidom.parseString( xmlData )

				# Get the HTTP url...
				playlistNode = xmldoc.documentElement.getElementsByTagName( "playList" )[0]
				clipNode     = playlistNode.getElementsByTagName( "clip" )[0]
				httpUriNode  = clipNode.getElementsByTagName( "httpURI" )[0]
				
				# SD or HD...
				video_url = httpUriNode.childNodes[0].nodeValue
				if (self.play_hd == "True") :
					video_url = video_url.replace( "_400.flv", "_1400.flv" )
				
				# cleanup
				playlistNode.unlink()

		#	
		# Play video...
		#
		playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
		playlist.clear()

		# only need to add label, icon and thumbnail, setInfo() and addSortMethod() takes care of label2
		listitem = xbmcgui.ListItem( self.video_title, iconImage="DefaultVideo.png", thumbnailImage=self.video_thumbnail )
		# set the key information
		listitem.setInfo( "video", { "Title": self.video_title, "Studio" : self.video_studio, "Plot" : self.video_plot, "Genre" : self.video_genre } )
		# add item to our playlist
		playlist.add( video_url, listitem )

		# Close wait dialog...
		dialogWait.close()
		del dialogWait
		
		# Play video...
		xbmcPlayer = xbmc.Player( self.video_players[ self.video_player ] )
		xbmcPlayer.play(playlist)   

#
# The End
#