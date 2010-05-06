from django.contrib import admin

from content.admin import ModelBaseAdmin

from music.models import AudioEmbed

admin.site.register(AudioEmbed, ModelBaseAdmin)
