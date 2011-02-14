from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from music.models import Track

class TrackImporter(object):
    def get_importer(self):
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
    
    def run(self):
        importer = self.get_importer()

        tracks = importer.run()

        for track in tracks:
            Track.objects.get_or_create(title=track.title)
            

