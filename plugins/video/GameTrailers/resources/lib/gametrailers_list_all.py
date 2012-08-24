#
# Imports
#
from BeautifulSoup      import BeautifulSoup, SoupStrainer
from gametrailers_const import __settings__, __language__
from gametrailers_utils import HTTPCommunicator
import httplib
import os
import re
import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin

#
# Main class
#
class Main:
	#
	# Init
	#
	def __init__( self ) :
		# Constants
		self.DEBUG       = False
		self.IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )
		self.PAGELIST_RE = re.compile( "(\d+) to (\d+) of \d+" )
		
		# Parse parameters...
		params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
		self.plugin_category =       params[ "plugin_category" ] 
		self.current_page    = int ( params.get( "page", "1" ) )
		
		# Settings
		self.video_quality   = __settings__.getSetting ("video_quality")


		#
		# Get the videos...
		#
		self.getVideos()
	
	#
	# Get videos...
	#
	def getVideos( self ) :
		#
		# Init
		#
				
		#
		# Get HTML page...
		#
		
		httpCommunicator = HTTPCommunicator()
		htmlData		 = httpCommunicator.get("http://www.gametrailers.com/fragments/line_listing_results/video_hub/?sortBy=most_recent&currentPage=%d" %  self.current_page)

		# Debug
		if (self.DEBUG) :
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "page_%i.html" % self.current_page), 'w')
			f.write( htmlData )
			f.close()

		# Parse response...
		beautifulSoup = BeautifulSoup( htmlData )
		
		#
		# Parse movie entries...
		#
		li_list = beautifulSoup.findAll ("li")
		for li in li_list:			
			div_video_information = li.find( "div", { "class" : "video_information" } )
			if (div_video_information == None) :
				continue
			
			# Title
			h4                    = div_video_information.find("h4")
			h4_a                  = h4.find("a")
			title                 = h4_a.string
			
			# Video page URL...
			video_page_url        = h4_a["href"]
			
			div_class_holder      = div_video_information.find( "div", { "class" : "holder" } )
			a_thumbnail           = div_class_holder.find( "a", { "class" : "thumbnail" } )
			img_thumbnail         = a_thumbnail.findAll( "img" ) [-1]
			thumbnail_url         = img_thumbnail[ "src" ]
			
			# Add to list...
			listitem        = xbmcgui.ListItem( title, iconImage = "DefaultVideo.png", thumbnailImage = thumbnail_url )
			listitem.setInfo( "video", { "Title" : title, "Studio" : "GameTrailers" } )
			plugin_play_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video_page_url ) )
			xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_play_url, listitem=listitem, isFolder=False)

		# Next page entry...
		listitem = xbmcgui.ListItem (__language__(30503), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'next-page.png'))
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = "%s?action=list-all&plugin_category=%s&page=%i" % ( sys.argv[0], self.plugin_category, self.current_page + 1 ), listitem = listitem, isFolder = True)

		# Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
		# End of directory...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

	#
	# Decode Platform
	#
	def decodePlatform( self, imageName ) :
		if (imageName.find("plat_arcade_default") > -1):
			return "Arcade"
		if (imageName.find("plat_pc_default") > -1):
			return "PC"
		if (imageName.find("plat_ps2_default") > -1):
			return "PS2"
		if (imageName.find("plat_ds_default") > -1):
			return "DS"
		if (imageName.find("plat_psp_default") > -1):
			return "PSP"
		if (imageName.find("plat_ps3_default") > -1):
			return "PS3"
		if (imageName.find("plat_ps1_default") > -1):
			return "PS1"
		if (imageName.find("plat_xbla_default") > -1):
			return "Xbox Live Arcade"
		if (imageName.find("plat_xb360_default") > -1):
			return "Xbox 360"
		if (imageName.find("plat_wii_default") > -1):
			return "Wii"
		if (imageName.find("plat_wiiware_default") > -1):
			return "WiiWare"
		if (imageName.find("plat_iphone_default") > -1):
			return "iPhone"
		if (imageName.find("plat_ipod_default") > -1):
			return "iPod"
		if (imageName.find("plat_vcon_default") > -1):
			return "Wii Virtual Console"
		if (imageName.find("plat_na_default") > -1 or imageName.find("plat__default") > -1):
			return "N/A"
		if (imageName.find("plat_psn_default") > -1):
			return "PSN"
		if (imageName.find("plat_xblcg_default") > -1):
			return "Xbox Live Community Games"
		return ""
