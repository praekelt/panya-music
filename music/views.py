from panya.generic.views import GenericObjectDetail
from music.models import AudioEmbed

class ListenLive(GenericObjectDetail):
    def get_queryset(self, *args, **kwargs):
        return AudioEmbed.permitted.all()
    
listen_live = ListenLive()
