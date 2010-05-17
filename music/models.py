from django.db import models

from ckeditor.fields import RichTextField
from content.models import ModelBase
from options.models import Options


# Content models
class AudioEmbed(ModelBase):
    embed = models.TextField()
    
    class Meta():
        verbose_name = "Audio Embed"
        verbose_name_plural = "Audio Embeds"
    
class Album(ModelBase):
    pass
        
class Credit(models.Model):
    contributor = models.ForeignKey(
        'music.TrackContributor',
        related_name='credits',
    )
    track = models.ForeignKey(
        'music.Track',
        related_name='credits',
    )
    role = models.IntegerField(
        blank=True,
        null=True,
    )
    
class TrackContributor(ModelBase):
    profile = RichTextField(
        blank=True,
        null=True,
    )
    track = models.ManyToManyField(
        'music.Track',
        through='music.Credit',
        related_name='contributors',
    )

class Track(ModelBase):
    contributor = models.ManyToManyField(
        'music.TrackContributor', 
        through='music.Credit',
        related_name='tracks',
    )
    album = models.ManyToManyField(Album)
    video_embed = models.TextField(
        blank=True,
        null=True,
    )

# Options models
class MusicOptions(Options):
    __module__ = 'options.models'
    
    class Meta:
        verbose_name = "Music Option"
        verbose_name_plural = "Music Options"

class MusicCreditOption(models.Model):
    music_options = models.ForeignKey('options.MusicOptions')
    role_name = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )
    role_priority = models.IntegerField(
        blank=True,
        null=True,
    )
