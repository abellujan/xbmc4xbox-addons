#
# Imports
#
import os
import sys
import re
import urllib
import base64
import time
import zipfile
import xbmc
import xbmcgui
import xbmcplugin

import sublight_utils as SublightUtils

#
#
#
class Main :
    def __init__( self ) :
        # Init
        debug = False
        
        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
        
        # Init
        session_id      = urllib.unquote_plus( params[ "session_id" ] )
        subtitle_id     = urllib.unquote_plus( params[ "subtitle_id" ] )
        subtitle_lang   = urllib.unquote_plus( params[ "subtitle_lang" ] )  
        number_of_discs = urllib.unquote_plus( params[ "number_of_discs" ] )
        movie_dir       = urllib.unquote_plus( params[ "movie_dir" ] )
        movie_file      = urllib.unquote_plus( params[ "movie_file" ] )
        
        # Subtitle directory...
        subtitle_dir = movie_dir
        if xbmcplugin.getSetting ("directory") == "1" \
           or movie_dir.startswith("http://") :             # Online movie
            subtitle_dir = xbmc.executehttpapi('GetGuiSetting(3;subtitles.custompath)').replace("<li>", "")
            if subtitle_dir == "" :
                subtitle_dir = movie_dir
        
        # Debug info
        if debug :
            print "=== sublight_download.py ==="
            print "SESSION ID         = " + session_id
            print "SUBTITLE ID        = " + subtitle_id
            print "SUBTITLE LANGUAGE  = " + subtitle_lang 
            print "NUMBER OF DISCS    = " + number_of_discs
            print "MOVIE DIR          = " + movie_dir
            print "MOVIE FILE         = " + movie_file
            print "SUBTITLE DIR       = " + subtitle_dir
            
        #
        # Wait dialog...
        #
        dp = xbmcgui.DialogProgress()
        dp.create("Sublight" )
        dp.update( 50, xbmc.getLocalizedString(30302), " ", " " )

        #
        # Get download ticket...
        #
        sublightWebService = SublightUtils.SublightWebService()
        ticket_id, download_wait = sublightWebService.GetDownloadTicket(session_id, subtitle_id)
        
        if debug :
            print "TICKET ID          = " + ticket_id
            print "DOWNLOAD WAIT      = " + download_wait
            
        if ticket_id != "" :
            #
            # Wait no seconds...
            #
            if download_wait > 0 :
                dp.update( 75, xbmc.getLocalizedString(30303) % download_wait, " ", " " )
                time.sleep(float(download_wait))
            
            #
            # Download subtitle...
            #
            subtitle_b64_data = sublightWebService.DownloadByID(session_id, subtitle_id, ticket_id)
            
            # Write BASE64 data in a file...
            base64_file_path = os.path.join( xbmc.translatePath( "special://temp" ), "subtitle.b64" )
            base64_file      = open(base64_file_path, "wb")
            base64_file.write( subtitle_b64_data )
            base64_file.close()
            
            # Re-open BASE64 file...
            base64_file = open(base64_file_path, "rb")
            
            # Open ZIP file... 
            zip_file_path = os.path.join( xbmc.translatePath( "special://temp" ), "subtitle.zip" )
            zip_file      = open(zip_file_path, "wb")
            
            # Decode subtitle data (BASE64 > ZIP)...            
            base64.decode(base64_file, zip_file)
            
            # Close files...
            base64_file.close()
            zip_file.close()
            
            # Close dialog...
            dp.close()
            
            
            #
            # Determine playing video file (used to set subtitle on the fly)...
            #
            playing_movie_file = None
            if xbmc.Player().isPlayingVideo() :
                playing_movie_file = os.path.split( xbmc.Player().getPlayingFile() )[1]  

            #
            # Determine the video files (prepare for renaming subtitles)...
            #
            movie_files     = []
            number_of_discs = int(number_of_discs)
            if number_of_discs == 1 :
                movie_files.append(movie_file)
            elif number_of_discs > 1 :
                # Determine the regular expression to match similar movie files...
                regexp = movie_file
                regexp = regexp.replace( "\\", "\\\\" )
                regexp = regexp.replace( "^", "\^" )
                regexp = regexp.replace( "$", "\$" )
                regexp = regexp.replace( "+", "\+" )
                regexp = regexp.replace( "*", "\*" )
                regexp = regexp.replace( "?", "\?" )
                regexp = regexp.replace( ".", "\." )
                regexp = regexp.replace( "|", "\|" )
                regexp = regexp.replace( "(", "\(" )
                regexp = regexp.replace( ")", "\)" )
                regexp = regexp.replace( "{", "\{" )
                regexp = regexp.replace( "}", "\}" )
                regexp = regexp.replace( "[", "\[" )
                regexp = regexp.replace( "]", "\]" )
                regexp = re.sub( "\d+", "\\d+", regexp )
                regex  = re.compile( regexp, re.IGNORECASE )
                
                # Find similar movie files...
                files = os.listdir( movie_dir )
                for file in files :
                    if regex.match( file ) != None:
                        movie_files.append(file)
                
                # Sort movie file list...
                movie_files.sort()
                
            #
            # Extract subtitle archive...
            #
            zip = zipfile.ZipFile (zip_file_path, "r")
            i   = 0
            for zip_entry in zip.namelist():
                # Rename the sub file to match the video files...
                file_name = zip_entry
                i         = i + 1
                if i <= len( movie_files ) :
                    sub_ext  = os.path.splitext( file_name )[1]
                    sub_name = os.path.splitext( movie_files[i - 1] )[0]
                
                try :
                    # Subtitle filename, including language...
                    file_name = "%s.%s%s" % ( sub_name, subtitle_lang, sub_ext )   
                    
                    # Write file...
                    file_path = os.path.join(subtitle_dir, file_name)
                    outfile   = open(file_path, "wb")
                    outfile.write( zip.read(zip_entry) )
                    outfile.close()
                    
                except IOError :
                    # Subtitle filename, excluding language...
                    file_name = "%s%s" % ( sub_name, sub_ext )   
                    
                    # Write file...
                    file_path = os.path.join(subtitle_dir, file_name)
                    outfile   = open(file_path, "wb")
                    outfile.write( zip.read(zip_entry) )
                    outfile.close()
            
                #
                # Set subtitle to current playing video...
                #
                if playing_movie_file != None :
                    if i <= len( movie_files ) and playing_movie_file == movie_files[ i - 1 ] :
                        xbmc.Player().setSubtitles( file_path )                    

            # Close zip archive...
            zip.close()
            
            #
            # Clean-up
            #
            os.remove(base64_file_path)
            os.remove(zip_file_path)
            
            #
            # The End
            #
            xbmcgui.Dialog().ok( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30306) + "\n" + subtitle_dir)

