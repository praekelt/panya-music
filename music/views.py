from content.generic.views import GenericObjectDetail
from music.models import AudioEmbed, Track

class ListenLive(GenericObjectDetail):
    def get_queryset(self):
        return AudioEmbed.permitted.all()
    
listen_live = ListenLive()

class PopupObjectDetail(GenericObjectDetail):
    def get_queryset(self):
        return Track.permitted.all()
    
    def get_template_name(self):
        return "music/popup/music_detail.html"
        
popup_object_detail = PopupObjectDetail()
