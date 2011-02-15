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
            handler = urlopen(url)
            size = handler.headers.get('content-length')
            data = handler.read()
            if hashlib.md5(data).hexdigest() not in INVALID_IMAGE_MD5: 
                f = cStringIO.StringIO()
                f.write(data)
                field_name = str(field)
                content_type=mimetypes.guess_type(file_name)[0]
                
                result = InMemoryUploadedFile(f, field_name, file_name, content_type, size, None)
                field.save(result.name, result)
                f.close()
    except Exception, e:
        logging.fatal("Unable to set image for %s: %s" % (artist_title, e))
