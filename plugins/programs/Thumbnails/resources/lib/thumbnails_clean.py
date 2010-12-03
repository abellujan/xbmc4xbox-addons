#
# Imports
#
import os
import sys
import glob
import time
import xbmc
import xbmcgui
import xbmcplugin

import traceback
from BeautifulSoup import BeautifulSoup

from urllib import quote_plus, unquote_plus
from os import linesep

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
        # Scan UserData\Thumbnails...
        #
        try :
            #
            # Init
            #
            THUMBNAILS_PATH = os.path.join( xbmc.translatePath("special://profile/"), "Thumbnails" )
            textboxControl  = self.getControl( 5 )
            output_text     = ""
            
            #
            # Start...
            #
            dialogProgress = xbmcgui.DialogProgress()
            dialogProgress.create( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30200) )

            #
            # (1) Thumbnails (top)...
            #
            dialogProgress.update( 1, xbmc.getLocalizedString(30200), "Thumbnails")
            topThumbPath                         = THUMBNAILS_PATH
            before_file_count, before_total_size = self.scanPath( topThumbPath )
            self.cleanThumbnailsFromPath( topThumbPath )
            after_file_count, after_total_size   = self.scanPath( topThumbPath )

            output_text = output_text + "Thumbnails"    + os.linesep
            output_text = output_text + "~~~~~~~~~~~~~" + os.linesep
            output_text = output_text + "Before = %u file(s), %s"   % ( before_file_count, self.formatSize( before_total_size ) ) + os.linesep
            output_text = output_text + "After    = %u file(s), %s" % ( after_file_count , self.formatSize( after_total_size  ) ) + os.linesep
            output_text = output_text + os.linesep
            textboxControl.setText( output_text )
            
            #
            # (2) Music thumbs (no cleanup)...
            #
            dialogProgress.update( 20, xbmc.getLocalizedString(30200), "Thumbnails\Music")
            musicThumbPath                       = os.path.join( THUMBNAILS_PATH, "Music" )
            before_file_count, before_total_size = self.scanPath( musicThumbPath )
            
            output_text = output_text + "Thumbnails\Music" + os.linesep
            output_text = output_text + "~~~~~~~~~~~~~"    + os.linesep
            output_text = output_text + "Before = %u file(s), %s"   % ( before_file_count, self.formatSize( before_total_size ) ) + os.linesep
            output_text = output_text + "After    = %u file(s), %s" % ( before_file_count, self.formatSize( before_total_size ) ) + os.linesep
            output_text = output_text + os.linesep
            textboxControl.setText( output_text )
            
            #
            # (3) Picture thumbs...
            #
            dialogProgress.update( 40, xbmc.getLocalizedString(30200), "Thumbnails\Pictures")
            picturesThumbPath                    = os.path.join( THUMBNAILS_PATH, "Pictures" )
            before_file_count, before_total_size = self.scanPath( picturesThumbPath )
            self.cleanThumbnailsFromPath( picturesThumbPath )
            after_file_count, after_total_size   = self.scanPath( picturesThumbPath )
            
            output_text = output_text + "Thumbnails\Pictures" + os.linesep
            output_text = output_text + "~~~~~~~~~~~~~"       + os.linesep
            output_text = output_text + "Before = %u file(s), %s"   % ( before_file_count, self.formatSize( before_total_size ) ) + os.linesep
            output_text = output_text + "After    = %u file(s), %s" % ( after_file_count , self.formatSize( after_total_size  ) ) + os.linesep
            output_text = output_text + os.linesep
            textboxControl.setText( output_text )
            
            #
            # (4) Program thumbnails...
            #
            dialogProgress.update( 60, xbmc.getLocalizedString(30200), "Thumbnails\Programs")
            programsThumbPath                    = os.path.join( THUMBNAILS_PATH, "Programs" )
            before_file_count, before_total_size = self.scanPath( programsThumbPath )
            self.cleanThumbnailsFromPath( programsThumbPath )
            after_file_count,  after_total_size  = self.scanPath( programsThumbPath )
            
            output_text = output_text + "Thumbnails\Programs" + os.linesep
            output_text = output_text + "~~~~~~~~~~~~~"       + os.linesep
            output_text = output_text + "Before = %u file(s), %s"   % ( before_file_count, self.formatSize( before_total_size ) ) + os.linesep
            output_text = output_text + "After    = %u file(s), %s" % ( after_file_count , self.formatSize( after_total_size  ) ) + os.linesep
            output_text = output_text + os.linesep
            textboxControl.setText( output_text )
            
            #
            # (5) Video thumbs...
            #
            dialogProgress.update( 80, xbmc.getLocalizedString(30200), "Thumbnails\Video")
            videoThumbPath                       = os.path.join( THUMBNAILS_PATH, "Video" )
            before_file_count, before_total_size = self.scanPath( videoThumbPath )
            
            #
            # Scan library...
            #
            exception_tbns = []
            
            # Library - Movies...
            movie_tbns = self.scanMovieLibrary()
            exception_tbns.extend( movie_tbns )
            
            # Library - TV Shows...
            tvshow_tbns = self.scanTvShowLibrary()
            exception_tbns.extend( tvshow_tbns )
            
            # Library - Episodes...
            episode_tbns = self.scanEpisodeLibrary()
            exception_tbns.extend( episode_tbns )
            
            # Library - Actors...
            actor_tbns = self.scanActorsLibrary();
            exception_tbns.extend( actor_tbns )
            
            # Clean video thumbnails...
            self.cleanThumbnailsFromPath( videoThumbPath, exception_tbns )
            after_file_count, after_total_size   = self.scanPath( videoThumbPath )
            
            output_text = output_text + "Thumbnails\Video" + os.linesep
            output_text = output_text + "~~~~~~~~~~~~~"    + os.linesep
            output_text = output_text + "Before = %u file(s), %s"   % ( before_file_count, self.formatSize( before_total_size ) ) + os.linesep
            output_text = output_text + "After    = %u file(s), %s" % ( after_file_count , self.formatSize( after_total_size  ) ) + os.linesep            
            textboxControl.setText( output_text )
            
            #
            # Finished...
            #
            dialogProgress.update( 100, "")
            dialogProgress.close()

            
        #
        # Aw :(
        #
        except Exception :
            dialogProgress.close()
            
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            output_text = repr(traceback.format_exception(exceptionType, exceptionValue, exceptionTraceback))
            
            textboxControl.setText( output_text )
            
        #
        # The end
        #

    
    #
    # Scan path for thumbnails...
    #
    def scanPath (self, path ):
        # Init
        files_count = 0
        files_size  = 0        
        
        # Scan folder (no sub-folders)... 
        if not os.path.isdir( os.path.join( path, "0" ) ) :
            tbn_files = glob.glob( os.path.join( path, "*.tbn" ) )
            for tbn_file in  tbn_files :
                statinfo    = os.stat( tbn_file )
                files_count = files_count + 1
                files_size  = files_size  + statinfo.st_size            
        # Scan sub-folders...
        else :
            for hexdigit in '01234567890ABCDEF' :
                thumb_dir = os.path.join( path, hexdigit )
                if os.path.isdir( thumb_dir ) :
                    tbn_files = glob.glob( os.path.join( thumb_dir, "*.tbn" ) )
                    for tbn_file in  tbn_files :
                        statinfo    = os.stat( tbn_file )
                        files_count = files_count + 1
                        files_size  = files_size  + statinfo.st_size
                    
        # Return value
        return files_count, files_size
        
    #
    # Clean thumbnails from path...
    #
    def cleanThumbnailsFromPath(self, path, exceptions = [] ):
        # Init
        files_count = 0
        files_size  = 0        
        
        # Scan folder (no sub-folders)...
        if not os.path.isdir( os.path.join( path, "0" ) ) :
            tbn_files = os.listdir( path )
            for tbn_file in tbn_files :
                if tbn_file.endswith( ".tbn" ) and \
                   not tbn_file in exceptions :
                    tbn_full_path = os.path.join( path, tbn_file )
                    statinfo      = os.stat( tbn_full_path )
                    
                    files_count   = files_count + 1
                    files_size    = files_size  + statinfo.st_size
                    
                    # Remove thumbnail...
                    os.remove( tbn_full_path )
                    
        # Scan sub-folders...
        else :            
            for hexdigit in '01234567890ABCDEF' :
                thumb_dir = os.path.join( path, hexdigit )
                if os.path.isdir( thumb_dir ) :
                    tbn_files = os.listdir( thumb_dir )
                    for tbn_file in tbn_files :
                        if tbn_file.endswith( ".tbn" ) and \
                           not tbn_file in exceptions :
                            tbn_full_path = os.path.join( path, tbn_file )
                            statinfo      = os.stat( tbn_full_path )
                            
                            files_count = files_count + 1
                            files_size  = files_size  + statinfo.st_size
                            
                            # Remove thumbnail...
                            os.remove( tbn_full_path )                    

    #
    #
    #
    def scanMovieLibrary(self):
        # Init...
        tbn_list = []
        
        # Get movie list...
        sql_movies = "select strPath, strFilename from movieview"
        movies_xml = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql_movies ), )
        
        beautifulSoup    = BeautifulSoup( movies_xml )
        fieldNodes       = beautifulSoup.findAll( "field" )
        fieldNodesTuples = zip( fieldNodes[::2], fieldNodes[1::2])
        for fieldNodePath, fieldNodeFile in  fieldNodesTuples:
            movie_path       = fieldNodePath.contents[0]
            movie_file       = fieldNodeFile.contents[0]
            movie_file_path  = os.path.join( movie_path, movie_file )
            
            tbn_movie_path       = xbmc.getCacheThumbName( movie_path )
            tbn_movie_file_path  = xbmc.getCacheThumbName( movie_file_path )
            
            tbn_list.append( tbn_movie_path )
            tbn_list.append( tbn_movie_file_path )            
            
        # Return TBN file list...
        return tbn_list
    
    #
    #
    #
    def scanActorsLibrary(self):         
        # Init...
        tbn_list = []
        
        # Get episode list...        
        sql_actors = "select strActor from actors"
        movies_xml = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql_actors ), )
        
        beautifulSoup = BeautifulSoup( movies_xml )
        fieldNodes    = beautifulSoup.findAll( "field" )
        for fieldNode in  fieldNodes:
            actor_name     = "actor" + str(fieldNode.contents[0]).lower()
            actor_name_tbn = xbmc.getCacheThumbName( actor_name )
        
            tbn_list.append( actor_name_tbn )
            
        # Return TBN file list...
        return tbn_list           
    
    #
    #
    #
    def scanTvShowLibrary(self):
        # Init...
        tbn_list = []
        
        # Get episode list...        
        sql_episodes = "select strPath from tvshowview"
        movies_xml = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql_episodes ), )
        
        beautifulSoup = BeautifulSoup( movies_xml )
        fieldNodes    = beautifulSoup.findAll( "field" )
        for fieldNode in  fieldNodes:
            tvshow_path     = fieldNode.contents[0]
            tbn_tvshow_path = xbmc.getCacheThumbName( tvshow_path )
            
            tbn_list.append( tbn_tvshow_path )
            
        # Return TBN file list...
        return tbn_list      

    #
    #
    #
    def scanEpisodeLibrary(self):
        # Init...
        tbn_list = []
        
        # Get episode list...        
        sql_episodes = "select strPath || strFilename from episodeview"
        movies_xml = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql_episodes ), )
        
        beautifulSoup = BeautifulSoup( movies_xml )
        fieldNodes    = beautifulSoup.findAll( "field" )
        for fieldNode in  fieldNodes:
            episode_full_path = fieldNode.contents[0]
            episode_thumbnail = xbmc.getCacheThumbName( episode_full_path )
            tbn_list.append( episode_thumbnail )
            
        # Return TBN file list...
        return tbn_list
                
    #
    # Format file size
    #
    def formatSize(self, size):
        SUFFIXES = [ 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        
        for suffix in SUFFIXES :
            size /= 1024
            if size < 1024 :
                return "%.1f %s" % ( size, suffix )

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
