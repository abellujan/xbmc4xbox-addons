#
# Imports
#
import os
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
		self.DEBUG = False
		
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
		# Play video...
		#
		self.playVideo()
	
	#
	# Play video...
	#
	def playVideo( self ) :
		if (self.DEBUG) :
			print "video_page_url = " + self.video_page_url

		#
		# Get current list item details...
		#
		title     = unicode( xbmc.getInfoLabel( "ListItem.Title"  ), "utf-8" )
		thumbnail =          xbmc.getInfoImage( "ListItem.Thumb"  )
		studio    = unicode( xbmc.getInfoLabel( "ListItem.Studio" ), "utf-8" )
		plot      = unicode( xbmc.getInfoLabel( "ListItem.Plot"   ), "utf-8" )
		genre     = unicode( xbmc.getInfoLabel( "ListItem.Genre"  ), "utf-8" )
		
		#
		# Show wait dialog while parsing data...
		#
		dialogWait = xbmcgui.DialogProgress()
		dialogWait.create( __language__(30403), title )			
		
		# 
		# Case 1: The id is part of the query (id=xyz) 
		# e.g. http://www.gamespot.com/xbox360/action/wanted/video_player.html?id=cSEynjOr5bIIvzTZ
		#
		if ("?id=" in self.video_page_url) :
			parsed     = urlparse(self.video_page_url)
			params     = dict(part.split('=') for part in parsed[4].split('&'))
			video_id   = params[ "id" ]
			video_url = "http://userimage.gamespot.com/cgi/deliver_user_video.php?id=%s" % ( video_id )
			
		#
		# Case 2: The id is part of the URL (id=1234567)
		# e.g. /ps3/action/killzone2/video/6205378/killzone-2-video-review
		#
		else :
			url_dict = self.video_page_url.split( "/" )
			if len( url_dict ) > 2 :
				video_id   = int( url_dict[ len(url_dict) - 2 ] )

				#
				# Call xml.php to get the address to the .FLV movie...
				#
				httpCommunicator = HTTPCommunicator()
				xml_php_url = "http://www.gamespot.com/pages/video_player/xml.php?id=%s" % str( video_id )
				xmlData     = httpCommunicator.get( xml_php_url )
				
				# Add the xml declaration + character encoding (missing)...
				xmlData = "<?xml version=\"1.0\" encoding=\"iso8859-1\" ?>" + os.linesep + xmlData
		
				# Debug
				if (self.DEBUG) :
					f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "xml_php_reply.xml"), 'w')
					f.write( xmldoc.toxml() )
					f.close()
		
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
		if (self.DEBUG) :
			print "Playing : " + video_url
		
		playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
		playlist.clear()

		# set the default icon
		icon = "DefaultVideo.png"
		# only need to add label, icon and thumbnail, setInfo() and addSortMethod() takes care of label2
		listitem = xbmcgui.ListItem( title, iconImage=icon, thumbnailImage=thumbnail )
		# set the key information
		listitem.setInfo( "video", { "Title": title, "Studio" : studio, "Plot" : plot, "Genre" : genre } )
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