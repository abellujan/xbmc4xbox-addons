import os
import xbmc
import xbmcplugin

#
# Constants
# 
__settings__    = xbmcplugin
__language__    = xbmc.getLocalizedString
__images_path__ = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )