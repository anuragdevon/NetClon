from django.db import models
from django.db.models.fields import proxy

class Video(models.Model):
    video_title = models.CharField(max_length=400)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=400) # id associated with it not pk
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.video_title

# Proxy Model
class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'All Video'
        verbose_name_plural = 'All Videos'

class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published Video'
