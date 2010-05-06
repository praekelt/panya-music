Django Music
============
**Django music app.**

Installation
------------

#. Add *music* to your *INSTALLED_APPS* setting.

#. Add music url include to the project's url.py file::

    (r'^music/', include('music.urls')),

#. Add a *LISTEN_LIVE_AUDIO_EMBED_ID* to the project's *settings.py* file in the form::

    # Id of AudioEmbed object to use in django-music's listen_live view.
    LISTEN_LIVE_AUDIO_EMBED_ID = '198'


Usage
-----

A listen live popup utilizing the audio embed object specified in your settings can be access through */music/listen-live*
