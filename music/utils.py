import cStringIO
import hashlib
import logging
import mimetypes
import os
from urllib import urlopen

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

import pylast

INVALID_IMAGE_MD5 = [
    '28fa757eff47ecfb498512f71dd64f5f',
]
        
def set_image_via_lastfm(artist_title, field):
    try:
        network = pylast.LastFMNetwork(api_key=settings.LASTFM_API_KEY, api_secret=settings.LASTFM_API_SECRET)
        artist = network.get_artist(artist_title)
        image_url = artist.get_cover_image()
        url = artist.get_cover_image()
        if url:
            file_name = '.'.join([artist_title, url.split('.')[-1]]).replace('/', '-')
            data = urlopen(url).read()
            if hashlib.md5(data).hexdigest() not in INVALID_IMAGE_MD5: 
                relative_path = field[0].upload_to('', file_name)
                f = open(os.path.join(settings.MEDIA_ROOT, relative_path), 'w')
                f.write(data)
                f.close()
                return relative_path
    except Exception, e:
        print "Unable to set image for %s: %s" % (artist_title, e)
        logging.fatal("Unable to set image for %s: %s" % (artist_title, e))
