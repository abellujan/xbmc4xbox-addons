#
# Imports
#
import os
import md5
import time
import array
import httplib
import xbmc
import xml.dom.minidom

#
# Integer => Hexadecimal
#
def dec2hex(n, l=0):
    # return the hexadecimal string representation of integer n
    s = "%X" % n
    if (l > 0) :
        while len(s) < l:
            s = "0" + s 
    return s

#
# Hexadecimal => integer
#
def hex2dec(s):
    # return the integer value of a hexadecimal string s
    return int(s, 16)

#
# String => Integer
#
def toInteger (string):
    try:
        return int( string )
    except :
        return 0

#
# Calculate MD5 partial video hash (not used)...
#
def calculateMD5VideoHash(filename):
    #
    # Check file...
    #
    if not os.path.isfile(filename) :
        return ""
     
    if os.path.getsize(filename) < 5 * 1024 * 1024 :
        return ""

    #
    # Calculate MD5 hash of the first 5 MB of video data...
    #
    f       = open(filename, mode="rb")
    md5hash = md5.new()
    for i in range(1, 6) :
        buffer = f.read( 1024 * 1024 )
        md5hash.update(buffer)
    f.close()

    # Return value (hex)
    return md5hash.hexdigest()

#
# Calculate Sublight video hash...
#
def calculateVideoHash(filename, isPlaying = False):
    #
    # Check file...
    #
    if not os.path.isfile(filename) :
        return ""
    
    if os.path.getsize(filename) < 5 * 1024 * 1024 :
        return ""

    #
    # Init
    #
    sum = 0
    hash = ""
    
    #
    # Byte 1 = 00 (reserved)
    #
    number = 0
    sum = sum + number
    hash = hash + dec2hex(number, 2) 
    
    #
    # Bytes 2-3 (video duration in seconds)
    #
    
    # Playing video...
    if isPlaying == True :
        seconds = int( xbmc.Player().getTotalTime() )
    # Selected video...
    else :
        player = xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER)
        player.play(filename)
        counter = 0
        while not player.isPlaying() and counter < 3 :
            time.sleep(1)
            counter = counter + 1
        seconds = int(player.getTotalTime())
        player.stop()
    
    # 
    sum = sum + (seconds & 0xff) + ((seconds & 0xff00) >> 8)
    hash = hash + dec2hex(seconds, 4)
    
    #
    # Bytes 4-9 (video length in bytes)
    #
    filesize = os.path.getsize(filename)
    
    sum = sum + (filesize & 0xff) + ((filesize & 0xff00) >> 8) + ((filesize & 0xff0000) >> 16) + ((filesize & 0xff000000) >> 24)
    hash = hash + dec2hex(filesize, 12) 
    
    #
    # Bytes 10-25 (md5 hash of the first 5 MB video data)
    #
    f       = open(filename, mode="rb")
    md5hash = md5.new()
    for i in range( 1, 41 ) :
        buffer = f.read( 128 * 1024 )           # 128 KB
        md5hash.update(buffer)
    buffer = None
    f.close()
    
    #
    array_md5 = array.array('B')
    array_md5.fromstring(md5hash.digest())
    for b in array_md5 :
        sum = sum + b

    hash = hash + md5hash.hexdigest()
    
    #
    # Byte 26 (control byte)
    # 
    hash = hash + dec2hex(sum % 256, 2)
    hash = hash.upper()
    
    return hash

#
# Detect movie title and year from file name...
#
def getMovieTitleAndYear( filename ):
    name = os.path.splitext( filename )[0]

    cutoffs = ['dvdrip', 'dvdscr', 'cam', 'r5', 'limited',
               'xvid', 'h264', 'x264', 'h.264', 'x.264',
               'dvd', 'screener', 'unrated', 'repack', 'rerip', 
               'proper', '720p', '1080p', '1080i', 'bluray']

    # Clean file name from all kinds of crap...
    for char in ['[', ']', '_', '(', ')']:
        name = name.replace(char, ' ')
    
    # if there are no spaces, start making beginning from dots...
    if name.find(' ') == -1:
        name = name.replace('.', ' ')
    if name.find(' ') == -1:
        name = name.replace('-', ' ')
    
    # remove extra and duplicate spaces!
    name = name.strip()
    while name.find('  ') != -1:
        name = name.replace('  ', ' ')
        
    # split to parts
    parts = name.split(' ')
    year = ""
    cut_pos = 256
    for part in parts:
        # check for year
        if part.isdigit():
            n = int(part)
            if n>1930 and n<2050:
                year = part
                if parts.index(part) < cut_pos:
                    cut_pos = parts.index(part)
                
        # if length > 3 and whole word in uppers, consider as cutword (most likelly a group name)
        if len(part) > 3 and part.isupper() and part.isalpha():
            if parts.index(part) < cut_pos:
                cut_pos = parts.index(part)
                
        # check for cutoff words
        if part.lower() in cutoffs:
            if parts.index(part) < cut_pos:
                cut_pos = parts.index(part)
        
    # make cut
    name = ' '.join(parts[:cut_pos])
    return name, year

#
# Convert from plugin language id => Sublight language
#
def toSublightLanguage(id):
    languages = { "0" : "None",
                  "1" : "Albanian",
                  "2" : "Arabic",
                  "3" : "Belarusian",
                  "4" : "BosnianLatin",
                  "5" : "Bulgarian",
                  "6" : "Catalan",
                  "7" : "Chinese",
                  "8" : "Croatian",
                  "9" : "Czech",
                  "10" : "Danish",
                  "11" : "Dutch",
                  "12" : "English",
                  "13" : "Estonian",
                  "14" : "Finnish",
                  "15" : "French",
                  "16" : "German",
                  "17" : "Greek",
                  "18" : "Hebrew",
                  "19" : "Hindi",
                  "20" : "Hungarian",
                  "21" : "Icelandic",
                  "22" : "Indonesian",
                  "23" : "Irish",
                  "24" : "Italian",
                  "25" : "Japanese",
                  "26" : "Korean",
                  "27" : "Latvian",
                  "28" : "Lithuanian",
                  "29" : "Macedonian",
                  "30" : "Norwegian",
                  "31" : "Persian",
                  "32" : "Polish",
                  "33" : "Portuguese",
                  "34" : "PortugueseBrazil",
                  "35" : "Romanian",
                  "36" : "Russian",
                  "37" : "SerbianLatin",
                  "38" : "Slovak",
                  "39" : "Slovenian",
                  "40" : "Spanish",
                  "41" : "SpanishArgentina",
                  "42" : "Swedish",
                  "43" : "Thai",
                  "44" : "Turkish",
                  "45" : "Ukrainian",
                  "46" : "Vietnamese",
                }
    return languages[ id ]
    
#
# SublightWebService class
#
class SublightWebService :
    def __init__ (self):
        self.CLIENT_ID                  = "XBMC"
        self.API_KEY                    = "195CCC1E-FB37-4619-84C5-67A787E3EBD3"
        
        self.SOAP_HOST                  = "www.sublight.si"
        self.SOAP_SUBTITLES_API_URL     = "/API/WS/Sublight.asmx"
        
        self.LOGIN_ANONYMOUSLY_ACTION   = "http://www.sublight.si/LogInAnonymous4"
        self.SUGGEST_TITLES             = "http://www.sublight.si/SuggestTitles"
        self.SEARCH_SUBTITLES_ACTION    = "http://www.sublight.si/SearchSubtitles3"
        self.GET_DOWNLOAD_TICKET_ACTION = "http://www.sublight.si/GetDownloadTicket"
        self.DOWNLOAD_BY_ID_ACTION      = "http://www.sublight.si/DownloadByID4"
        self.LOGOUT_ACTION              = "http://www.sublight.si/LogOut"
        
    #
    # Perform SOAP request...
    #
    def SOAP_POST (self, SOAPUrl, SOAPAction, SOAPRequestXML):
            # Handles making the SOAP request
            h = httplib.HTTPConnection(self.SOAP_HOST)
            headers = {
                'Host'           : self.SOAP_HOST,
                'Content-Type'   :'text/xml; charset=utf-8',
                'Content-Length' : len(SOAPRequestXML),
                'SOAPAction'     : '"%s"' % SOAPAction,
            }
            h.request ("POST", SOAPUrl, body=SOAPRequestXML, headers=headers)
            r = h.getresponse()
            d = r.read()
            h.close()
            
            if r.status != 200:
                raise ValueError('Error connecting: %s, %s' % (r.status, r.reason))
            
            return d
    
    #
    # LoginAnonymous3
    #
    def LogInAnonymous(self):
        # Build request XML...
        requestXML = """<?xml version="1.0" encoding="utf-8"?>
                        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
                                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                                       xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                          <soap:Body>
                            <LogInAnonymous4 xmlns="http://www.sublight.si/">
                              <clientInfo>
                                <ClientId>%s</ClientId>
                                <ApiKey>%s</ApiKey>
                              </clientInfo>
                            </LogInAnonymous4>
                          </soap:Body>
                        </soap:Envelope>""" % ( self.CLIENT_ID, self.API_KEY )
        
        # Call SOAP service...
        resultXML = self.SOAP_POST (self.SOAP_SUBTITLES_API_URL, self.LOGIN_ANONYMOUSLY_ACTION, requestXML)
        
        # Parse result
        resultDoc = xml.dom.minidom.parseString(resultXML)
        xmlUtils  = XmlUtils()
        sessionId = xmlUtils.getText( resultDoc, "LogInAnonymous4Result" )
        
        # Return value
        return sessionId


    #
    # LogOut
    #
    def LogOut(self, sessionId):
        # Build request XML...
        requestXML = """<?xml version="1.0" encoding="utf-8"?>
                        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
                                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                                       xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                          <soap:Body>
                            <LogOut xmlns="http://www.sublight.si/">
                              <session>%s</session>
                            </LogOut>
                          </soap:Body>
                        </soap:Envelope>""" % ( sessionId )
                          
        # Call SOAP service...
        resultXML = self.SOAP_POST (self.SOAP_SUBTITLES_API_URL, self.LOGOUT_ACTION, requestXML)
        
        # Parse result
        resultDoc = xml.dom.minidom.parseString(resultXML)
        xmlUtils  = XmlUtils()
        result    = xmlUtils.getText( resultDoc, "LogOutResult" )
        
        # Return value
        return result
    
    #
    # SuggestTitles
    #
    def SuggestTitles( self, keywords ):
        # Build request XML...
        requestXML = """<?xml version="1.0" encoding="utf-8"?>
                        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
                                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                                       xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                          <soap:Body>
                            <SuggestTitles xmlns="http://www.sublight.si/">
                              <keyword>%s</keyword>
                              <itemsCount>%u</itemsCount>
                            </SuggestTitles>
                          </soap:Body>
                        </soap:Envelope>""" % ( keywords,
                                                15 )
                        
        # Call SOAP service...
        resultXML = self.SOAP_POST (self.SOAP_SUBTITLES_API_URL, self.SUGGEST_TITLES, requestXML)
        
        # Parse result
        resultDoc = xml.dom.minidom.parseString(resultXML)
        xmlUtils  = XmlUtils() 
        result    = xmlUtils.getText(resultDoc, "SuggestTitlesResult")
        
        titles = []      
        if (result == "true") :
            imdbNodes = resultDoc.getElementsByTagName( "IMDB" )
            for imdbNode in imdbNodes :
                title  = xmlUtils.getText( imdbNode, "Title" )
                year   = xmlUtils.getText( imdbNode, "Year" )
                titles.append( { "title" : title, "year" : year } )
                    
        # Return value
        return titles

    #
    # SearchSubtitles
    #
    def SearchSubtitles(self, sessionId, videoHash, title, year, language1, language2, language3):
        # Build request XML...
        requestXML = """<?xml version="1.0" encoding="utf-8"?>
                        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                                       xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                          <soap:Body>
                            <SearchSubtitles3 xmlns="http://www.sublight.si/">
                              <session>%s</session>
                              <videoHash>%s</videoHash>
                              <title>%s</title>
                              %s
                              <season xsi:nil="true" />
                              <episode xsi:nil="true" />
                              <languages>
                                %s
                                %s
                                %s
                              </languages>
                              <genres>
                                <Genre>Movie</Genre>
                                <Genre>Cartoon</Genre>
                                <Genre>Serial</Genre>
                                <Genre>Documentary</Genre>
                                <Genre>Other</Genre>
                                <Genre>Unknown</Genre>
                              </genres>
                              <rateGreaterThan xsi:nil="true" />
                            </SearchSubtitles3>
                          </soap:Body>
                        </soap:Envelope>""" % ( sessionId, 
                                                videoHash,
                                                title,
                                                ( "<year>%s</year>" % year, "<year xsi:nil=\"true\" />" ) [ year == "" ],
                                                  "<SubtitleLanguage>%s</SubtitleLanguage>" % language1,
                                                ( "<SubtitleLanguage>%s</SubtitleLanguage>" % language2, "" ) [ language2 == "None" ],
                                                ( "<SubtitleLanguage>%s</SubtitleLanguage>" % language3, "" ) [ language3 == "None" ] )
        
        # Call SOAP service...
        resultXML = self.SOAP_POST (self.SOAP_SUBTITLES_API_URL, self.SEARCH_SUBTITLES_ACTION, requestXML)
        
        # Parse result
        resultDoc = xml.dom.minidom.parseString(resultXML)
        xmlUtils  = XmlUtils() 
        result    = xmlUtils.getText(resultDoc, "SearchSubtitles3Result")
        
        subtitles = []      
        if (result == "true") :
            # Releases...
            releases = dict()
            releaseNodes = resultDoc.getElementsByTagName("Release")
            if releaseNodes != None :
                for releaseNode in releaseNodes :
                    subtitleID  = xmlUtils.getText( releaseNode, "SubtitleID" )
                    releaseName = xmlUtils.getText( releaseNode, "Name" )
                    if releaseName > "" :
                        releases[ subtitleID ] = releaseName
            
            # Subtitles...
            subtitleNodes = resultDoc.getElementsByTagName("Subtitle")
            for subtitleNode in subtitleNodes:
                title         = xmlUtils.getText( subtitleNode, "Title" )
                year          = xmlUtils.getText( subtitleNode, "Year" )
                release       = releases.get( subtitleID, ("%s (%s)" % ( title, year  ) ) )
                language      = xmlUtils.getText( subtitleNode, "Language" )
                subtitleID    = xmlUtils.getText( subtitleNode, "SubtitleID" )
                mediaType     = xmlUtils.getText( subtitleNode, "MediaType" )
                numberOfDiscs = xmlUtils.getText( subtitleNode, "NumberOfDiscs" ) 
                downloads     = xmlUtils.getText( subtitleNode, "Downloads" )
                isLinked      = xmlUtils.getText( subtitleNode, "IsLinked" )              
                
                subtitles.append( { "title" : title, "year" : year, "release" : release, "language" : language, "subtitleID" : subtitleID, "mediaType" : mediaType, "numberOfDiscs" : numberOfDiscs, "downloads" : downloads, "isLinked" : isLinked } )            
            
        # Return value
        return subtitles        
    
    #
    # GetDownloadTicket
    #
    def GetDownloadTicket(self, sessionID, subtitleID):
        # Build request XML...
        requestXML = """<?xml version="1.0" encoding="utf-8"?>
                        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
                                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                                       xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                          <soap:Body>
                            <GetDownloadTicket xmlns="http://www.sublight.si/">
                              <session>%s</session>
                              <id>%s</id>
                            </GetDownloadTicket>
                          </soap:Body>
                        </soap:Envelope>""" % ( sessionID, subtitleID )
                        
        # Call SOAP service...
        resultXML = self.SOAP_POST (self.SOAP_SUBTITLES_API_URL, self.GET_DOWNLOAD_TICKET_ACTION, requestXML)
        
        # Parse result
        resultDoc = xml.dom.minidom.parseString(resultXML)
        xmlUtils  = XmlUtils()
        result    = xmlUtils.getText( resultDoc, "GetDownloadTicketResult" )
        
        ticket = ""
        if result == "true" :
            ticket = xmlUtils.getText( resultDoc, "ticket" )
            que    = xmlUtils.getText( resultDoc, "que" )
            
        # Return value
        return ticket, que
    
    #
    # DownloadByID3 
    #
    def DownloadByID(self, sessionID, subtitleID, ticketID):
        # Build request XML...
        requestXML = """<?xml version="1.0" encoding="utf-8"?>
                        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
                                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                                       xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                          <soap:Body>
                            <DownloadByID4 xmlns="http://www.sublight.si/">
                              <sessionID>%s</sessionID>
                              <subtitleID>%s</subtitleID>
                              <codePage>65001</codePage>
                              <removeFormatting>false</removeFormatting>
                              <ticket>%s</ticket>
                            </DownloadByID4>
                          </soap:Body>
                        </soap:Envelope>""" % ( sessionID, subtitleID, ticketID )

        # Call SOAP service...
        resultXML = self.SOAP_POST (self.SOAP_SUBTITLES_API_URL, self.DOWNLOAD_BY_ID_ACTION, requestXML)
        
        # Parse result
        resultDoc = xml.dom.minidom.parseString(resultXML)
        xmlUtils  = XmlUtils()
        result    = xmlUtils.getText( resultDoc, "DownloadByID4Result" )
        
        base64_data = ""
        if result == "true" :
            base64_data = xmlUtils.getText( resultDoc, "data" )
        
        # Return value
        return base64_data
        
#
#
#
class XmlUtils :
    def getText (self, nodeParent, childName ):
        # Get child node...
        node = nodeParent.getElementsByTagName( childName )[0]
        
        if node == None :
            return None
        
        # Get child text...
        text = ""
        for child in node.childNodes:
            if child.nodeType == child.TEXT_NODE :
                text = text + child.data
        return text
