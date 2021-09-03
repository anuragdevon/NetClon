from django.db import models

# Create your models here.
class Video(mdoels.Model):
  title = models.CharField()
  description = models.TextField()
  slug = models.SlugField(blank=True, null=True)
  video-id = models.CharField()
