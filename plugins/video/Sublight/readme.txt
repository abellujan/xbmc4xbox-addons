Sublight
~~~~~~~~
 v1.9 (Friday, 6 January 2012):
  - allow browsing for .mp4 files;
  - improved file name cleanup;
  - active download wait counter;
  - remember last browsed location;

 v1.85 beta (Thursday, 10 December 2010):
  - online movie / not scraped - ask the user for movie name when searching for playing movie;
  - online movies - save the subtitle in the local custom subtitle path; 

 v1.82 (Tuesday, 05 October 2010)
  - calculate MD5 in (even) smaller chunks (might benefit Xbox with large skins while playing video);
  - Italian translation (thanks to KymyA);

 v1.8 (30 April 2010):
  - Sublight API changes;
  - calculate MD5 in smaller chunks (might benefit Xbox with large skins);

 v1.71 (26 October 2009) :
  - set downloaded subtitle for playing movie; 

 v1.7 (18 September 2009):
  - [xbox] if subtitle filename including language is too long, try again without language;

 v1.6 (15 August 2009):
  - server moved to http://www.sublight.si 

 v1.5 (5 July 2009) :
  - add "Search for playing movie";

 v1.4 (5 July 2009 ):
  - workaround to avoid crashing XBMC on Linux (use GetFullVideoHash() method);
  - use movie name when searching (thanks to queeup, credits to FlexGet);
  - add option to search by title;
  - add language to the subtitle file name;

 v1.35 :
  - always use the full video hash;
  - not handling correctly empty text XML nodes;  

 v1.2 :
  - allow to choose subtitles destination (movie directory or XBMC custom directory);
  - rename subtitle(s) to match video file(s);
  - when GetFullVideoHash not returning a video hash, fallback to xbmc.Player() method;
  - highlight (green) "linked" subtitles;

 v1.1 :
  - alternate way of calculating the video hash (no need to play the video);