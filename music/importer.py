from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from music.models import MusicCreditOption, Track

class TrackImporter(object):
    def get_importer(self):
        """
        Resolve importer from TRACK_IMPORTER_CLASS setting.
        """
        try:
            importer_path = settings.TRACK_IMPORTER_CLASS
        except AttributeError:
            raise ImproperlyConfigured('No TRACK_IMPORTER_CLASS setting found.')
        try:
            dot = importer_path.rindex('.')
        except ValueError:
            raise ImproperlyConfigured('%s isn\'t a Track Importer module.' % importer_path)
        module, classname = importer_path[:dot], importer_path[dot+1:]
        try:
            mod = import_module(module)
        except ImportError, e:
            raise ImproperlyConfigured('Could not import Track Importer %s: "%s".' % (module, e))
        try:
            importer_class = getattr(mod, classname)
        except AttributeError:
            raise ImproperlyConfigured('Track Importer module "%s" does not define a "%s" class.' % (module, classname))
   
        importer_instance = importer_class()
        if not hasattr(importer_instance, 'run'):
            raise ImproperlyConfigured('Track Importer class "%s" does not define a run method. Implement the method to return a list of Track objects.' % classname)
        
        return importer_instance

    def lookup_track(self, track):
        """
        Looks up Django Track object for provided raw importing track object.
        """
        tracks = Track.objects.filter(title__iexact=track.title)
        for track_obj in tracks:
            for contributor in track_obj.get_primary_contributors(permitted=False):
                if contributor.title == track.artist:
                    return track_obj
        return None
    
    def run(self):
        """
        Run import.
        """
        latest_track = Track.objects.all().order_by('-last_played')
        latest_track = latest_track[0] if latest_track else None
        
        importer = self.get_importer()
        tracks = importer.run()

        # Create/update Django Track objects for importer tracks.
        for track in tracks:
            # Only create/update if tracks with start times greater than what already exists are imported. 
            if not latest_track or track.start_time > latest_track.last_played:
                obj = self.lookup_track(track)
                # Don't update importing track that is regarded as the latest. This prevents start times from constantly incrementing.
                if latest_track and obj == latest_track:
                    print "[%s-%s]: Start time not updated as it is the latest track." % (track.title, track.artist)
                    continue

                # If no existing track object could be resolved, create it.
                if not obj:
                    print "[%s-%s]: Created." % (track.title, track.artist)
                    obj = Track.objects.create(title=track.title)
                    obj.length = track.length
                    roles = MusicCreditOption.objects.all().order_by('role_priority') 
                    role = roles[0].role_priority if roles else 1
                    obj.create_credit(track.artist, role)
                else:
                    print "[%s-%s]: Not created as it already exists." % (track.title, track.artist)
                
                # Update last played time to start time.
                obj.last_played = track.start_time
                obj.save()
                print "[%s-%s]: Start time updated to %s." % (track.title, track.artist, track.start_time)
            else:
                print "[%s-%s]: Not created as it has a past start time of %s (latest %s). " % (track.title, track.artist, track.start_time, latest_track.last_played)
