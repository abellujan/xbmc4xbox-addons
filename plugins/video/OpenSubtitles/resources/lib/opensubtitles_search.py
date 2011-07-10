#
# Imports
#
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xmlrpclib
import struct
import urllib

#
# Main class
#
class Main:
    #
    # Init
    #
    def __init__( self ):
        #
        # Constants
        #
        self.IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )

        #
        # Parse parameters...
        #
        params        = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))        
        movieFullPath = urllib.unquote_plus( params.get( "movie_file", "" ) )
        
        #
        # Get subtitles...
        #
        self.getSubtitles( movieFullPath )
    
    #
    # Get subtitles...
    #
    def getSubtitles(self, movieFullPath = ""):
        
        # Init
        token      = None
        resultData = None
        
        #
        # Browse for movie file (when not playing)...
        #
        if movieFullPath == "" :
            browse = xbmcgui.Dialog()
            movieFullPath = browse.browse(1, xbmc.getLocalizedString(30200), "video", ".avi|.mpg|.mpeg|.wmv|.asf|.divx|.mov|.m2p|.moov|.omf|.qt|.rm|.vob|.dat|.dv|.3ivx|.m2ts|.mkv|.ogm")
        
            # No file selected...
            if movieFullPath == "" :
                xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=False )
                return
        
        #
        # Languages (prepare filter)...
        #
        sub_language1 = self.toOpenSubtitlesId( str( int( xbmcplugin.getSetting ("sub_language1") ) + 1 ) )
        sub_language2 = self.toOpenSubtitlesId(           xbmcplugin.getSetting ("sub_language2") )
        sub_language3 = self.toOpenSubtitlesId(           xbmcplugin.getSetting ("sub_language3") )
        sub_languages = []
        sub_languages.append( sub_language1 )
        if sub_language2 != "none" :
            sub_languages.append( sub_language2 )
        if sub_language3 != "none" :
            sub_languages.append(sub_language3)        
        
        #
        # Movie dir...
        #
        movie_dir  = os.path.dirname  (movieFullPath)
        movie_file = os.path.basename (movieFullPath)
        
        #
        # Calculate file hash code...
        #
        hashResult = self._calcHash(movieFullPath)
                
        try :
            #
            # Logging in...
            #
            dialogProgress = xbmcgui.DialogProgress()
            dialogProgress.create( "OpenSubtitles" )
            dialogProgress.update( 25, xbmc.getLocalizedString(30201) )
            
            server = xmlrpclib.Server( "http://api.opensubtitles.org/xml-rpc", verbose=0 )
            #print server.ServerInfo()        
            login  = server.LogIn("", "", "en", "XBMC OpenSubtitles Plugin v1.2")
            
            status = login[ "status" ]
            token  = login[ "token"  ]
            
            if status != "200 OK" :
                errorDialog = xbmcgui.Dialog()
                errorDialog.ok("OpenSubtitles", xbmc.getLocalizedString(30204), xbmc.getLocalizedString(30205) )
                del errorDialog
                
                xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=False )
                return
        except Exception, e:
            errorDialog = xbmcgui.Dialog()
            errorDialog.ok("OpenSubtitles", xbmc.getLocalizedString(30204), xbmc.getLocalizedString(30205) )
            del errorDialog
            
            xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=False )
            return
        
        #
        # Searching...
        #
        try :
            dialogProgress.update( 50, xbmc.getLocalizedString(30202), movie_file, "" )            

            # Language #1
            searchArray = []
            searchArray.append( { "sublanguageid" :      sub_languages[0], 
                                  "moviehash"     :      hashResult[ "moviehash" ],
                                  "moviebytesize" : str( hashResult[ "moviesize" ] ) } )
            
            # Language #2
            if len(sub_languages) > 1 :
                searchArray.append( { "sublanguageid" :      sub_languages[1], 
                                      "moviehash"     :      hashResult[ "moviehash" ],
                                      "moviebytesize" : str( hashResult[ "moviesize" ] ) } )
            
            # Language #3
            if len(sub_languages) > 2 :
                searchArray.append( { "sublanguageid" :      sub_languages[2], 
                                      "moviehash"     :      hashResult[ "moviehash" ],
                                      "moviebytesize" : str( hashResult[ "moviesize" ] ) } )
            
            # Search...
            resultData = server.SearchSubtitles( token, searchArray )
                
        except :
            errorDialog = xbmcgui.Dialog()
            errorDialog.ok("OpenSubtitles", xbmc.getLocalizedString(30204), xbmc.getLocalizedString(30205) )
            del errorDialog

            xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=False )
            return

        #
        # Logging out...
        #
        try :
            dialogProgress.update( 75, xbmc.getLocalizedString(30203) )
            server.LogOut(token)        
            dialogProgress.close()
            del dialogProgress
        except :
            pass

        #
        # Process results...
        #
        if resultData :
            #
            # No results...
            #
            if resultData[ "data" ] == False :
                dialog = xbmcgui.Dialog()
                dialog.ok("OpenSubtitles", xbmc.getLocalizedString(30206), "")
                
                # End of list...
                xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=False )
                
            #
            # Results found...
            #            
            else:
                subtitles = resultData[ "data" ] 
                for subtitle in subtitles:
                    subFileName     = subtitle[ "SubFileName" ]
                    subLanguageID   = subtitle[ "SubLanguageID" ]
                    subLanguageName = subtitle[ "LanguageName" ]
                    subSumCD        = subtitle[ "SubSumCD" ]
                    subDownloadsCnt = subtitle[ "SubDownloadsCnt" ]
                    zipDownloadURL  = subtitle[ "ZipDownloadLink" ]
                    icon_flag       = os.path.join( self.IMAGES_PATH, "flag_%s.gif" % subLanguageID.lower()) 

                    # Add directory entry...
                    label    = "[%s] %s" % ( subLanguageID, subFileName )
                    label2   = "%s downloads [%s x CD]" % ( subDownloadsCnt, subSumCD )
                    listitem = xbmcgui.ListItem( label, label2, "DefaultVideoBig.png", icon_flag )
                    listitem.setInfo( type="Video", infoLabels={ "Title" : label, "Genre" : label2 } )
                    url      = "%s?action=download&language_name=%s&num_cds=%s&download_url=%s&movie_dir=%s&movie_file=%s" % \
                               ( sys.argv[ 0 ], urllib.quote_plus( subLanguageName ), urllib.quote_plus( subSumCD), urllib.quote_plus( zipDownloadURL ), urllib.quote_plus( movie_dir ), urllib.quote_plus( movie_file ) )
                    xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=url, listitem=listitem, isFolder=False)
            
                # Allow sort by Genre (for list2 labels)...
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
                
                # End of list (success)...
                xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

    #
    #
    #
    def _calcHash(self, filename): 
        try:
            longlongformat = 'q'  # long long
            bytesize = struct.calcsize(longlongformat)
            
            f = open(filename, "rb")
            
            filesize = os.path.getsize(filename)
            hash = filesize 
                    
            if filesize < 65536 * 2: 
                return "SizeError" 
                 
            for x in range(65536/bytesize): 
                buffer = f.read(bytesize) 
                (l_value,)= struct.unpack(longlongformat, buffer)  
                hash += l_value 
                hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number  
                         
            f.seek(max(0,filesize-65536),0) 
            for x in range(65536/bytesize): 
                buffer = f.read(bytesize) 
                (l_value,)= struct.unpack(longlongformat, buffer)  
                hash += l_value 
                hash = hash & 0xFFFFFFFFFFFFFFFF 
                 
            f.close() 
            returnedhash = "%016x" % hash 
            
            return { "moviehash" : returnedhash, "moviesize" : filesize }
    
        except(IOError): 
            return "IOError"
        
    #
    # Convert from plugin language id (settings) => OpenSubtitles language id...
    #
    def toOpenSubtitlesId( self, id ):
        languages = { "0"  : "none",
                      "1"  : "alb",
                      "2"  : "ara",
                      "3"  : "arm",
                      "4"  : "bos",
                      "5"  : "bul",
                      "6"  : "cat",
                      "7"  : "chi",
                      "8"  : "hrv",
                      "9"  : "cze",
                      "10" : "dan",
                      "11" : "dut",
                      "12" : "eng",
                      "13" : "epo",
                      "14" : "est",
                      "15" : "per",
                      "16" : "fin",
                      "17" : "fre",
                      "18" : "glg",
                      "19" : "geo",
                      "20" : "ger",
                      "21" : "ell",
                      "22" : "heb",
                      "23" : "hin",
                      "24" : "hun",
                      "25" : "ice",
                      "26" : "ind",
                      "27" : "ita",
                      "28" : "jpn",
                      "29" : "kaz",
                      "30" : "kor",
                      "31" : "lav",
                      "32" : "lit",
                      "33" : "ltz",
                      "34" : "mac",
                      "35" : "may",
                      "36" : "nor",
                      "37" : "oci",
                      "38" : "pol",
                      "39" : "por",
                      "40" : "pob",
                      "41" : "rum",
                      "42" : "rus",
                      "43" : "scc",
                      "44" : "slo",
                      "45" : "slv",
                      "46" : "spa",
                      "47" : "swe",
                      "48" : "syr",
                      "49" : "tha",
                      "50" : "tur",
                      "51" : "ukr",
                      "52" : "urd",
                      "53" : "vie"
                    }
        return languages[ id ]
