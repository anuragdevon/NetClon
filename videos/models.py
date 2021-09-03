from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Models for videos
class Video(models.Model):
    class VideoStateOptions(models.TextChoices):    ###
      PUBLISH = 'PU', 'Publish'
      DRAFT = 'DR', 'Draft'

# system break after commit - "add state options"    ###
  # Colums
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True) ###
    video_id = models.CharField(max_length=220, unique=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=VideoStateOptions.choices) ###
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    @property
    def is_published(self):
        return self.active

  # Specifying how to save      ###
    def save(self, *args, **kwargs):
        if self.state == self.VideoStateOptions.PUBLISH and self.publish_timestamp is None:
            print("Save as timestamp as published")
            self.published_timestamp = timezone.now()

        elif self.state == self.VideoStateOptions.DRAFT:
            self.publish_timestamp = None
            if self.slug == None:
                self.slug = slugify(self.title)
            super().save(*args, **kwargs) ###

# Video Proxy
class VideoAllProxy(Video): ###
  class Meta:
    proxy = True
    verbose_name = 'All Video'
    verbose_name_plural = 'All Videos'

# Published videos proxy
class VideoPublishedProxy(Video):
  class Meta:
    proxy = True
    verbose_name = 'Published Video'
