from django.conf import settings
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'music.views',
    url(r'^listen-live/$', 'listen_live', {'object_id': getattr(settings, 'LISTEN_LIVE_AUDIO_EMBED_ID', '-1') }, name='music_listen_live'),
    url(r'^popup/(?P<slug>[\w-]+)/$', 'popup_object_detail', name='music_popup_object_detail'),
)
