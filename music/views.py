from content.generic.views import GenericObjectDetail
from music.models import AudioEmbed

class ListenLive(GenericObjectDetail):
    def get_queryset(self):
        return AudioEmbed.permitted.all()
    
listen_live = ListenLive()
