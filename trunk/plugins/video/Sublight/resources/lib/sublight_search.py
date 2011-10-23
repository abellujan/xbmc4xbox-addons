import sublight_utils as SublightUtils

import os
import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin

#
#
#
class Main :
    def __init__( self ) :
        #
        # Init
        #
        IMAGES_PATH        = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )
        sublightWebService = SublightUtils.SublightWebService()
        
        #
        # Parse parameters...
        #
        params   = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))        
        searchBy = params[ "search_by" ]

        #
        # Playing movie...
        #
        if searchBy == "playing" :
            movieFullPath = xbmc.Player().getPlayingFile()
        #
        # Browse for movie file...
        #
        else :
            # Get last location (get up one level if path doesn't exist anymore)...
            lastMoviePath = xbmcplugin.getSetting ("lastMoviePath")
            while lastMoviePath != ""   and         \
                  lastMoviePath != "\\" and         \
                  not os.path.exists(lastMoviePath) :
                lastMoviePath = os.path.dirname(lastMoviePath)
            
            # Browse dialog...
            browse = xbmcgui.Dialog()
            movieFullPath = browse.browse(1, xbmc.getLocalizedString(30200), "video", ".avi|.mp4|.mpg|.mpeg|.wmv|.asf|.divx|.mov|.m2p|.moov|.omf|.qt|.rm|.vob|.dat|.dv|.3ivx|.mkv|.ogm", False, False, lastMoviePath)
            
            # No file selected (exit)...
            if not os.path.isfile(movieFullPath) :
                xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=False )
                return

            # Save last location...
            lastMoviePath = os.path.join(os.path.dirname(movieFullPath), "")
            xbmcplugin.setSetting("lastMoviePath", lastMoviePath)

        # Split in dir and filename...
        movie_dir  = os.path.dirname  (movieFullPath)
        movie_file = os.path.basename (movieFullPath)
        
        #
        # (By Title) Confirm movie title...
        #
        movie_title, movie_year = "", ""
        if searchBy == "title" :
            # Attempt to extract the movie title and year from the file name... 
            movie_title, movie_year = SublightUtils.getMovieTitleAndYear( movie_file )            
            
            #
            # Get a list of similar titles from the webservice...
            #
            movies = sublightWebService.SuggestTitles( movie_title )

            # Ask the user to choose a movie entry...
            if len( movies ) > 0:
                options = []
                for movie in movies :
                   option = "%s (%s)" % ( movie[ "title" ], movie [ "year" ] )
                   options.append( option )
                   
                dialog = xbmcgui.Dialog()
                choice = dialog.select( xbmc.getLocalizedString(30307), options )
                dialog = None
                
                # User made a choice...
                if choice > -1 :
                    movie       = movies[ choice ];
                    movie_title = movie[ "title"]
                    movie_year  = movie[ "year" ]
                # User cancelled...
                else :
                    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=False )
                    return
            #             
            # No matching results...
            #
            else :
                #
                # Ask the user to confirm movie title and year...
                #
                if movie_year != "" :
                    text = "%s (%s)" % ( movie_title, movie_year )
                else :
                    text = "%s"      % ( movie_title )
                            
                keyboard = xbmc.Keyboard( text )
                keyboard.doModal()
                if keyboard.isConfirmed() :
                    movie_title, movie_year = SublightUtils.getMovieTitleAndYear( keyboard.getText() )
                else :
                    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=False )
                    return
        
        #
        # (WebService) Login...
        #
        dp = xbmcgui.DialogProgress()
        dp.create("Sublight" )
        dp.update( 33, xbmc.getLocalizedString(30300), " ", " " )        
        
        # Get session id...
        session_id = sublightWebService.LogInAnonymous()

        #
        # (By video hash) Calculate video hash...
        #
        video_hash = "0000000000000000000000000000000000000000000000000000"
        if searchBy == "hash" :
            video_hash     = SublightUtils.calculateVideoHash( movieFullPath, False )
        
        #
        # (By playing movie) Calculate video hash...
        #
        if searchBy == "playing" :
            videoInfoTag = xbmc.Player().getVideoInfoTag()
            movie_title = videoInfoTag.getTitle()
            movie_year  = ( videoInfoTag.getYear(), "" ) [ videoInfoTag.getYear() == 0 ]
            
            # No movie title, ask user...
            if movie_title == "" :
                keyboard = xbmc.Keyboard( "", xbmc.getLocalizedString(30107) )
                keyboard.doModal()
                if keyboard.isConfirmed() :
                    movie_title, movie_year = SublightUtils.getMovieTitleAndYear( keyboard.getText() )
            
            # Calculate hash...
            video_hash  = SublightUtils.calculateVideoHash( movieFullPath, True )
        
        #
        # (WebService) Search...
        #
        if searchBy == "hash" :
            message = movie_file
        elif searchBy == "title" :                                                            
            message = ( "%s (%s)" % ( movie_title, movie_year ), "%s" % ( movie_title ) ) [ movie_year == "" ]
        elif searchBy == "playing" :
            message = ( "%s (%s)" % ( movie_title, movie_year ), "%s" % ( movie_file ) )  [ movie_year == "" ]
        dp.update( 66, xbmc.getLocalizedString(30301), message, " " )

        # Searching...
        subtitles = []
        language1 = SublightUtils.toSublightLanguage( str( int( xbmcplugin.getSetting ("language1") ) + 1 ) )
        language2 = SublightUtils.toSublightLanguage(           xbmcplugin.getSetting ("language2") )
        language3 = SublightUtils.toSublightLanguage(           xbmcplugin.getSetting ("language3") )
        subtitles = sublightWebService.SearchSubtitles(session_id, video_hash, movie_title, movie_year, language1, language2, language3 )
        
        #
        # No subtitles found...
        #
        if len(subtitles) == 0 :
            # Close dialog progress...
            dp.close()
            
            # Message...
            dialog = xbmcgui.Dialog()
            dialog.ok("Sublight", xbmc.getLocalizedString(30305))
            dialog = None

            # End of directory...
            xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=False )
            
        #
        # Subtitles found...
        #
        else:
            for subtitle in subtitles:
                subtitle_id   =                          subtitle[ "subtitleID" ]
                title         =                          subtitle[ "title" ]
                year          = SublightUtils.toInteger( subtitle[ "year" ] )
                release       =                          subtitle[ "release" ]
                language      =                          subtitle[ "language" ]
                mediaType     =                          subtitle[ "mediaType" ]
                numberOfDiscs = SublightUtils.toInteger( subtitle[ "numberOfDiscs" ] )
                downloads     =                          subtitle[ "downloads" ]
                isLinked      =                          subtitle[ "isLinked" ]                
                icon_flag     = os.path.join( IMAGES_PATH, "flag_%s.gif" % language.lower())
                
                # Add directory entry...
                label  = "[%s]  %s" % ( language, release )
                if isLinked == "true" :
                    label2 = "[COLOR=FF00FF00]%s downloads [%u x %s][/COLOR]" % ( downloads, numberOfDiscs, mediaType )
                else:
                    label2 = "%s downloads [%u x %s]" % ( downloads, numberOfDiscs, mediaType )
                
                listitem = xbmcgui.ListItem( label, label2, "DefaultVideoBig.png", icon_flag )
                listitem.setInfo( type="Video", infoLabels={ "Title" : label, "Genre" : label2, "Year" : year  } )
                url = "%s?action=download&session_id=%s&subtitle_id=%s&subtitle_lang=%s&movie_dir=%s&movie_file=%s&number_of_discs=%u" % \
                    ( sys.argv[ 0 ], urllib.quote_plus( session_id ), urllib.quote_plus( subtitle_id ), urllib.quote_plus( language ), urllib.quote_plus( movie_dir ), urllib.quote_plus( movie_file ), numberOfDiscs )
                xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url=url, listitem=listitem, isFolder=False)
    
            # Allow sort by Genre (for list2 labels)...
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )            
        
            # End of directory...
            xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
