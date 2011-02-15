from django.db import models

from ckeditor.fields import RichTextField
from music import utils
from panya.models import ModelBase
from preferences.models import Preferences
import pylast

# Content models
class AudioEmbed(ModelBase):
    embed = models.TextField()
    
    class Meta():
        verbose_name = "Audio embed"
        verbose_name_plural = "Audio embeds"
    
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
        help_text='Full profile for this contributor.',
        blank=True,
        null=True,
    )
    track = models.ManyToManyField(
        'music.Track',
        through='music.Credit',
        related_name='contributors',
    )
    def save(self, *args, **kwargs):
        if not self.image:
            utils.set_image_via_lastfm(self.title, self.image)
        super(TrackContributor, self).save(*args, **kwargs)

class Track(ModelBase):
    contributor = models.ManyToManyField(
        'music.TrackContributor', 
        through='music.Credit',
        related_name='tracks',
    )
    album = models.ManyToManyField(
        Album,
        blank=True,
        null=True,
    )
    video_embed = models.TextField(
        blank=True,
        null=True,
        help_text="A video embed script related to the track. Ensure the video is set to 422 x 344.",
    )
    last_played = models.DateTimeField(
        blank=True,
        null=True,
    )
    length = models.IntegerField(
        blank=True,
        null=True,
        help_text="Length of track in seconds."
    )

    def get_primary_contributors(self, permitted=True):
        """
        Returns a list of primary contributors, with primary being defined as those contributors that have the highest role assigned(in terms of priority). When permitted is set to True only permitted contributors are returned.
        """
        primary_credits = []
        credits = self.credits.exclude(role=None).order_by('role')
        if credits:
            primary_role = credits[0].role
            for credit in credits:
                if credit.role == primary_role:
                    primary_credits.append(credit)

        contributors = []
        for credit in primary_credits:
            contributor = credit.contributor
            if permitted and contributor.is_permitted:
                contributors.append(contributor)
            else:
                contributors.append(contributor)

        return contributors

    def create_credit(self, contributor_title, role):
        contributor, created = TrackContributor.objects.get_or_create(title=contributor_title)
        credit, created = Credit.objects.get_or_create(contributor=contributor, track=self, role=role)
        return credit, contributor

# Options models
class MusicPreferences(Preferences):
    __module__ = 'preferences.models'
    
    class Meta:
        verbose_name = "Music preferences"
        verbose_name_plural = "Music preferences"

class MusicCreditOption(models.Model):
    music_preferences = models.ForeignKey('preferences.MusicPreferences')
    role_name = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )
    role_priority = models.IntegerField(
        blank=True,
        null=True,
    )
