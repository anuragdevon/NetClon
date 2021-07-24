from django.db import models
from django.db.models.fields import proxy
from django.test.testcases import TestCase
from django.utils import timezone
from django.utils.text import slugify
class Video(models.Model):
    class VideoStateOptions(models.TextChoices):
        PUBLISH = 'PU', 'Pubish'
        DRAFT = 'DR', 'Draft'

    video_title = models.CharField(max_length=400)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=400, unique=True) # id associated with it not pk
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    state  = models.CharField(
                max_length=2,
                choices=VideoStateOptions.choices,
                default = VideoStateOptions.DRAFT)

    publish_timestamp = models.DateTimeField(
                auto_now_add=False,
                auto_now=False,
                blank=True,
                null = True)

    def __str__(self):
        return self.video_title

    @property
    def is_published(self):
        return self.active

    def save(self, *args, **kwargs):
        if self.state == self.VideoStateOptions.PUBLISH and self.publish_timestamp is None:
            print("Save as timestamp for published")
            self.publish_timestamp = timezone.now()
        elif self.state == self.VideoStateOptions.DRAFT:
            self.publish_timestamp = None

        if self.slug is None:
            self.slug = slugify(self.video_title)
        super.save(*args, **kwargs)


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
