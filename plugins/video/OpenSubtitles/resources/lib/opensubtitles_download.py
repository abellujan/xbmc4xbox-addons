#
# Imports
#
import os
import re
import sys
import urllib
import zipfile
import xbmc
import xbmcgui
import xbmcplugin

#
# Main class
#
class Main:
    def __init__(self) :
        # Init
        debug = False
        
        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
        
        # Init
        language_name = urllib.unquote_plus( params[ "language_name" ] )
        num_cds       = urllib.unquote_plus( params[ "num_cds" ] )
        download_url  = urllib.unquote_plus( params[ "download_url" ] )
        movie_dir     = urllib.unquote_plus( params[ "movie_dir" ] )
        movie_file    = urllib.unquote_plus( params[ "movie_file" ] )
        zip_local     = os.path.join( xbmc.translatePath( "special://temp" ), "opensubtitles.zip" )

        # Subtitle directory...
        subtitle_dir = movie_dir
        if xbmcplugin.getSetting ("sub_directory") == "1" :
            subtitle_dir = xbmc.executehttpapi('GetGuiSetting(3;subtitles.custompath)').replace("<li>", "")
            if subtitle_dir == "" :
                subtitle_dir = movie_dir

        # Debug info
        if debug :
            print "=== opensubtitles_download.py ==="
            print "LANGUAGE     = " + language_name
            print "DOWNLOAD URL = " + download_url
            print "MOVIE DIR    = " + movie_dir
            print "MOVIE FILE   = " + movie_file
            print "ZIP LOCAL    = " + zip_local
            print "SUBTITLE DIR = " + subtitle_dir


        # Download subtitles...
        self.download_subtitle ( download_url, zip_local )

        # Extract subtitles...
        self.extract_subtitle  ( zip_local, movie_dir, movie_file, subtitle_dir, language_name, num_cds )

    #
    # Download zip subtitle...
    #
    def download_subtitle(self, download_url, zip_local) :
        dp = xbmcgui.DialogProgress()
        dp.create(xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30207), download_url )
        urllib.urlretrieve( download_url, zip_local, lambda nb, bs, fs, url=download_url : self.download_progress_hook( nb, bs, fs, zip_local, dp ) )
        dp.close()

    #
    # Download progressbar handler...
    #
    def download_progress_hook(self, numblocks, blocksize, filesize, url=None, dp=None, ratio=1.0 ):
        try:
            percent = min( ( numblocks * blocksize * 100) / filesize, 100 )
            dp.update( int( percent * ratio ) )
        except:
            percent = 100
            dp.update( int( percent * ratio ) )
        if dp.iscanceled():
            raise IOError

    #
    # Extract zip subtitle...
    #
    def extract_subtitle( self, zip_local, movie_dir, movie_file, subtitle_dir, language_name, num_cds ):
        #
        # Check if a zip file (and not a "503 Service Unavailable" webpage)...
        #
        if not zipfile.is_zipfile( zip_local ) :
            # Error message...
            xbmcgui.Dialog().ok( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30208), xbmc.getLocalizedString(30209) )
            
            # Cleanup
            os.remove( zip_local )
            
            # Return...
            return
        
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
        num_cds = int( num_cds )
        if num_cds == 1 :
            movie_files.append( movie_file )
        elif num_cds > 1 :
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
        # Extract subtitle zip...
        #
        zip = zipfile.ZipFile (zip_local, "r")
        i   = 0
        for zip_entry in zip.namelist():
            zip_entry_ext = os.path.splitext( zip_entry )[1]
            
            # Ignore non-subtitle files...
            if zip_entry_ext in [ ".sub", ".srt" ] :
                #
                # Rename the sub file to match the video files...
                #
                file_name = zip_entry
                i         = i + 1
                if i <= len( movie_files ) :
                    sub_ext  = os.path.splitext( file_name )[1]
                    sub_name = os.path.splitext( movie_files[i - 1] )[0]   

                try :
                    #
                    # Subtitle filename, including language...
                    #
                    file_name = "%s.%s%s" % ( sub_name, language_name, sub_ext )                    
                    
                    #
                    # Write file (with language)...
                    #
                    file_path = os.path.join(subtitle_dir, file_name)
                    outfile = open(file_path, "wb")
                    outfile.write( zip.read(zip_entry) )
                    outfile.close()
                    
                except IOError :
                    #
                    # Subtitle filename, excluding language...
                    #                    
                    file_name = "%s%s" % ( sub_name, sub_ext )                 
                
                    #
                    # Write file (without language)...
                    #
                    file_path = os.path.join(subtitle_dir, file_name)
                    outfile = open(file_path, "wb")
                    outfile.write( zip.read(zip_entry) )
                    outfile.close()
                    
                #
                # Set subtitle to current playing video...
                #
                if playing_movie_file != None :
                    if i <= len( movie_files ) and playing_movie_file == movie_files[ i - 1 ] :
                        xbmc.Player().setSubtitles( file_path )
        
        #
        # Close ZIP...
        #        
        zip.close()
        
        #
        # Cleanup
        #
        os.remove( zip_local )
        
        #
        # Done
        #
        xbmcgui.Dialog().ok( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30210) + "\n" + subtitle_dir)

#
# EOF
#