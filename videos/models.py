from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save

from netflix.db.models import PublishStateOptions
from netflix.db.recievers import publish_state_pre_save, slugify_pre_save

# Create Custom Querysets
class VideoQuerySet(models.QuerySet):     ###
    def published(self):
        now = timezone.now()
        # return self.filter(state=Video.VideoStateOptions.PUBLISH, publish_timestamp__lte=now)
        return self.filter(state=PublishStateOptions.PUBLISH, publish_timestamp__lte=now)

# Create Custom Mangers
class VideoManager(models.Manager):      ###
    def get_queryset(self):
      return VideoQuerySet(self.model, using=self._db)

    def published(self):
      return self.get_queryset().published()


# Models for videos
class Video(models.Model):
    # class VideoStateOptions(models.TextChoices):    ###
    #   PUBLISH = 'PU', 'Publish'
    #   DRAFT = 'DR', 'Draft'

# system break after commit - "add state options"    ###
  # Colums
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True) ###
    video_id = models.CharField(max_length=220, unique=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT) ###
    # state = models.CharField(max_length=2, choices=VideoStateOptions.choices, default=PublishStateOptions.DRAFT) ###
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    # VideoManager
    objects = VideoManager()

    @property     ###
    def is_published(self):
        return self.active

    def get_playlist_ids(self):       ###
      return list(self.playlist_set.all().values_list('id', flat=True))     ###

  # # Specifying how to save      ###
  #   def save(self, *args, **kwargs):
  #       if self.state == self.VideoStateOptions.PUBLISH and self.publish_timestamp is None:
  #           print("Save as timestamp as published")
  #           self.published_timestamp = timezone.now()

  #       elif self.state == self.VideoStateOptions.DRAFT:
  #           self.publish_timestamp = None
  #           if self.slug == None:
  #               self.slug = slugify(self.title)
  #           super().save(*args, **kwargs) ###

# Video Proxy
class VideoAllProxy(Video): ###
  class Meta:
    proxy = True
    verbose_name = 'All Video'
    verbose_name_plural = 'All Videos'

# Published videos proxy
class VideoPublishedProxy(Video):     ###
  class Meta:
    proxy = True
    verbose_name = 'Published Video'
    verbose_name_plural = 'Published Videos'

# Invoking django signals
pre_save.connect(publish_state_pre_save, sender=Video)
pre_save.connect(slugify_pre_save, sender=Video)
