from django.test import TestCase
from django.utils import timezone

from .models import Video

# class VideoModelTestCase(TestCase):
#     def setUp(self):
#         Video.objects.create(video_title="Interstellar")
    
#     def test_valid_title(self):
#         title = "Interstellar"
#         qs = Video.objects.filter(video_title=title)
#         self.assertTrue(qs.exists())

#     def test_created_count(self):
#         qs = Video.objects.all()
#         self.assertEqual(qs.count(), 1)

class VideoModeltestCase(TestCase):
    def setUp(self):
        Video.objects.create(video_title='Star Wars')
        Video.objects.create(video_title="Star Wart", state=Video.VideoStateOptions.PUBLISH)

        def test_valid_title(self):
            title = 'Star Wart'

        def test_createed_count(self):
            qs = Video.objects.all()
            self.assertEqual(qs.count(), 2)

        def test_draft_case(self):
            qs = Video.objects.filter(state=Video.VideoStateOptions.DRAFT)
            self.assertEqual(qs.count(), 1)

        def test_publish_case(self):
            qs = Video.objects.filter(state=Video.VideoStateOptions.PUBLISH)
            now = timezone.now()
            published_qs = Video.objects.filter(
                            state=Video.VideoStateOptions.PUBLISH,
                            publish_timestamp__lte=now
            )
            self.assertTrue(published_qs.exists()) 