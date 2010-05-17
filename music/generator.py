import random

from generate import IMAGES
from generate.json_loader import load_json

ALBUM_COUNT = 20
CONTRIBUTOR_COUNT = 3
CREDIT_COUNT = 40
TRACK_CONTRIBUTOR_COUNT = 40
TRACK_COUNT = 20

CONTRIBUTOR_ROLE = [[1, "Artist"], [2, "Producer"], [3, "Composer"]]

def generate():
    objects = []
    
    # generate music options objects
    for i in range(0, CONTRIBUTOR_COUNT):
        contributor_role = CONTRIBUTOR_ROLE[i]
        objects.append({
            "model": "music.MusicCreditOption",
            "fields": {
                "role_priority": contributor_role[0],
                "role_name": contributor_role[1],
                "music_options": {
                    "model": "options.MusicOptions",
                    "fields": { 
                        "id": "1"
                    }
                },
            },
        })
    
    # generate track contributor objects
    for i in range(1, ALBUM_COUNT + 1):
        objects.append({
            "model": "music.Album",
            "fields": {
                "title": "Album %s Title" % i,
                "description": "Album %s description with some added text to verify truncates where needed." % i,
                "state": "published",
                "image": random.sample(IMAGES, 1)[0],
                "sites": {
                    "model": "sites.Site",
                    "fields": { 
                        "name": "example.com"
                    }
                },
            },
        })
    
    # generate track object
    for i in range(1, TRACK_COUNT + 1):
        objects.append({
            "model": "music.Track",
            "fields": {
                "title": "Track %s Title" % i,
                "description": "Track %s description with some added text to verify truncates where needed." % i,
                "state": "published",
                "image": random.sample(IMAGES, 1)[0],
                "video_embed": "",
                "sites": {
                    "model": "sites.Site",
                    "fields": { 
                        "name": "example.com"
                    }
                },
                "album": {
                    "model": "music.Album",
                    "fields": {
                        "title": "Album %s Title" % random.randint(1, ALBUM_COUNT),
                    }
                },
            },
        })
    
    # generate track contributor objects
    for i in range(1, TRACK_CONTRIBUTOR_COUNT + 1):
        objects.append({
            "model": "music.TrackContributor",
            "fields": {
                "title": "Track Contributor %s Title" % i,
                "description": "Track Contributor %s description with some added text to verify truncates where needed." % i,
                "state": "published",
                "image": random.sample(IMAGES, 1)[0],
                "sites": {
                    "model": "sites.Site",
                    "fields": { 
                        "name": "example.com"
                    }
                },
            },
        })
    
    # generate track credit objects
    for i in range(1, CREDIT_COUNT + 1):
        contributor_role = random.choice(CONTRIBUTOR_ROLE)
        objects.append({
            "model": "music.Credit",
            "fields": {
                "role": contributor_role[0],
                "track": {
                    "model": "music.Track",
                    "fields": { 
                        "title": "Track %s Title" % random.randint(1, TRACK_COUNT),
                    }
                },
                "contributor": {
                    "model": "music.TrackContributor",
                    "fields": {
                        "title": "Track Contributor %s Title" % i,
                    }
                },
            },
        })
    
    load_json(objects)
