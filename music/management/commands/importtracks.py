from django.core.management.base import BaseCommand, CommandError

from music.importer import TrackImporter

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:
            importer = TrackImporter()
            importer.run()
        except Exception, e:
            raise CommandError(e)
 
