from django.db import models
from django.utils import timezone

# Models for videos
class Video(models.Model):
  class VideoStateOptions(models.TextChoices): ###
    PUBLISH = 'PU', 'Publish'
    DRAFT = 'DR', 'Draft'

  # Colums
  title = models.CharField(max_length=220)
  description = models.TextField(blank=True, null=True)
  slug = models.SlugField(blank=True, null=True) ###
  video_id = models.CharField(max_length=220)
  active = models.BooleanField(default=True)
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
