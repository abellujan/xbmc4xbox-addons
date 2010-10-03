import os
import xbmc
import zlib
import httplib
import urllib
import urllib2
import gzip
import StringIO
import HTMLParser

#
# XBMC constants
#
result       = xbmc.executehttpapi('GetSystemInfoByName(system.buildversion;system.builddate)')
system_info  = result.split('<li>')
XBMC_BUILD_VERSION = system_info[1]
XBMC_BUILD_DATE    = system_info[2]

#
# HTTPCommunicator
#
class HTTPCommunicator :
    #
    # POST
    #
    def post( self, host, url, params ):
        parameters  = urllib.urlencode( params )
        headers     = { "Content-type"    : "application/x-www-form-urlencoded",
                        "Accept"          : "text/plain",
                        "Accept-Encoding" : "gzip" }
        connection  = httplib.HTTPConnection("%s:80" % host)
        
        connection.request( "POST", url, parameters, headers )
        response = connection.getresponse()
        
        # Compressed (gzip) response...
        if response.getheader( "content-encoding" ) == "gzip" :
            htmlGzippedData = response.read()
            stringIO       = StringIO.StringIO( htmlGzippedData )
            gzipper        = gzip.GzipFile( fileobj = stringIO )
            htmlData       = gzipper.read()
        # Plain text response...
        else :
            htmlData = response.read()

        # Cleanup
        connection.close()

        # Return value
        return htmlData

    #
    # GET
    #
    def get( self, url ):
        h = urllib2.HTTPHandler(debuglevel=0)
        
        request = urllib2.Request( url )
        request.add_header( "Accept"         , "*/*" )
        request.add_header( "Accept-Encoding", "gzip" )
        request.add_header( "User-Agent"     , "Python-urllib/%s (%s; XBMC/%s, %s)" % ( urllib2.__version__, os.name.upper(), XBMC_BUILD_VERSION, XBMC_BUILD_DATE ) )
        opener = urllib2.build_opener(h)
        f = opener.open(request)

        # Compressed (gzip) response...
        if f.headers.get( "content-encoding" ) == "gzip" :
            htmlGzippedData = f.read()
            stringIO        = StringIO.StringIO( htmlGzippedData )
            gzipper         = gzip.GzipFile( fileobj = stringIO )
            htmlData        = gzipper.read()
            
            # Debug
            # print "[HTTP Communicator] GET %s" % url
            # print "[HTTP Communicator] Result size : compressed [%u], decompressed [%u]" % ( len( htmlGzippedData ), len ( htmlData ) )
            
        # Plain text response...
        else :
            htmlData = f.read()
        
        # Cleanup
        f.close()

        # Return value
        return htmlData
    
#
# Convert HTML to readable strings...
#
class HTML2Text :
    #
    #
    #
    def convert( self, html ):
        text = html.replace( "&nbsp;", " " )
        return text.strip()

#
# HTMLStripper class - strip HTML tags from text
#
class HTMLStripper (HTMLParser.HTMLParser):
    def __init__(self):
        self.reset()
        self.texts = []

    def handle_data(self, text):
        text = text.replace(u"\xa0", " ")
        text = text.replace(u"hr /", "")
        self.texts.append(text)
        
    def get_fed_data(self):
        return "".join(self.texts)
    