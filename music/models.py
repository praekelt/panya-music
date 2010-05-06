from django.db import models

from content.models import ModelBase

class AudioEmbed(ModelBase):
    embed = models.TextField()
    class Meta():
        verbose_name = "Audio Embed"
        verbose_name_plural = "Audio Embeds"
