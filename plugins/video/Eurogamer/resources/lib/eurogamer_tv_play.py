#
# Imports
#
import re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib
from BeautifulSoup      import SoupStrainer
from BeautifulSoup      import BeautifulSoup
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
		self.DEBUG = False
		
		# Parse parameters...
		params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
		self.video_page_url = urllib.unquote_plus( params[ "video_page_url" ] ) 

		# Settings
		self.video_players = { "0" : xbmc.PLAYER_CORE_AUTO,
							   "1" : xbmc.PLAYER_CORE_DVDPLAYER,
							   "2" : xbmc.PLAYER_CORE_MPLAYER }
		self.video_player = xbmcplugin.getSetting ("video_player")
		
		# Play video...
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
		dialogWait.create( xbmc.getLocalizedString(30402), title )	
		
		# 
		# Parse video HTML page to get the video URL... 
		#
		httpCommunicator = HTTPCommunicator()
		htmlSource       = httpCommunicator.get( self.video_page_url )
		
		# Debug
		if (self.DEBUG) :
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "video_page.html" ), "w")
			f.write( htmlSource )
			f.close()
		
		# Parse HTML page...
		soupStrainer  = SoupStrainer( "div", { "id" : "content" } )
		beautifulSoup = BeautifulSoup ( htmlSource, soupStrainer)
		div_player    = beautifulSoup.find( "div", { "id" : "player" } )
		scripts       = div_player.findAll( {"script" : True} )
		
		if len( scripts ) == 1 :
			script        = scripts[0].string.strip()
		
			# Get the URL for etgv.swf
			swf_object_regexp = re.compile( '"playlist_id", "(.*)"' )
			playlist_id       = swf_object_regexp.findall ( script )[0]
			swf_object_regexp = re.compile( '"profile_id", "(.*)"' )
			profile_id        = swf_object_regexp.findall ( script )[0]
			
		elif len( scripts ) == 0 :
			# Fallback to outer script...
			script = div_player.findNextSibling( "script" ).string.strip()
			
			# Get the URL for etgv.swf
			swf_object_regexp = re.compile( '"playlist_id", "(.*)"' )
			playlist_id       = swf_object_regexp.findall ( script )[0]
			swf_object_regexp = re.compile( '"profile_id", "(.*)"' )
			profile_id        = swf_object_regexp.findall ( script )[0]

		
		# Call get_pls.php with the playlist id & profile id...
		get_pls_url = "http://www.eurogamer.net/get_pls.php?playlist_id=%s&profile_id=%s" % ( playlist_id, profile_id )
		httpCommunicator = HTTPCommunicator()
		htmlSource       = httpCommunicator.get( get_pls_url )

		# Debug
		if (self.DEBUG) :
			print "GET_PLS URL = " + get_pls_url
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "get_pls_reply.html" ), "w")
			f.write( htmlSource )
			f.close()
		
		# Parse get_pls.php reply...
		reply_list = dict(part.split('=', 1) for part in htmlSource.split('&'))
		file_ids = reply_list[ "order" ].split(",")
		file_id  = file_ids[ len(file_ids) - 1 ]          # Get last video id (skip commercials)...
		video_url = reply_list[ "file[%s]" % file_id ]
		video_url = urllib.unquote( video_url )
		
		# Close wait dialog...
		dialogWait.close()
		del dialogWait
				
		#	
		# Play video...
		#		
		if (self.DEBUG) :
			print "Playing : " + video_url
		
		playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
		playlist.clear()

		# Set video info...
		listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
		listitem.setInfo( "video", { "Title": title, "Studio" : studio, "Plot" : plot, "Genre" : genre } )

		# Add item to our playlist...
		playlist.add( video_url, listitem )

		# Play...
		xbmcPlayer = xbmc.Player( self.video_players[ self.video_player ] ).play( playlist )		

#
# The End
#