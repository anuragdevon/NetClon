diff --git a/.gitignore b/.gitignore
index 60abaaa..9a75da8 100644
--- a/.gitignore
+++ b/.gitignore
@@ -1,5 +1,6 @@
-django/
+env/
 data/
 lite
 .lite_workspace.lua
 .lite_last_project
+netflix/__pycache__/
diff --git a/netflix/__pycache__/settings.cpython-39.pyc b/netflix/__pycache__/settings.cpython-39.pyc
index 79ec547..f919605 100644
Binary files a/netflix/__pycache__/settings.cpython-39.pyc and b/netflix/__pycache__/settings.cpython-39.pyc differ
diff --git a/netflix/settings.py b/netflix/settings.py
index b35fb50..a0f9ee6 100644
--- a/netflix/settings.py
+++ b/netflix/settings.py
@@ -30,7 +30,10 @@ ALLOWED_HOSTS = ['*']
 # Application definition
 
 INSTALLED_APPS = [
+    # my apps
     'videos.apps.VideosConfig',
+    'playlists.apps.PlaylistsConfig',
+    # django inbuilt apps
     'django.contrib.admin',
     'django.contrib.auth',
     'django.contrib.contenttypes',
diff --git a/videos/__pycache__/admin.cpython-39.pyc b/videos/__pycache__/admin.cpython-39.pyc
index b7b3747..cf0f409 100644
Binary files a/videos/__pycache__/admin.cpython-39.pyc and b/videos/__pycache__/admin.cpython-39.pyc differ
diff --git a/videos/__pycache__/models.cpython-39.pyc b/videos/__pycache__/models.cpython-39.pyc
index bd14a6b..5f6d537 100644
Binary files a/videos/__pycache__/models.cpython-39.pyc and b/videos/__pycache__/models.cpython-39.pyc differ
diff --git a/videos/admin.py b/videos/admin.py
index 8a12625..27dffab 100644
--- a/videos/admin.py
+++ b/videos/admin.py
@@ -5,10 +5,10 @@ from django.utils import timezone
 from .models import VideoAllProxy, VideoPublishedProxy
 
 class VideoAllAdmin(admin.ModelAdmin):
-    list_display = ['video_title', 'id', 'video_id', 'is_published']
+    list_display = ['video_title', 'id', 'video_id', 'is_published', 'get_playlist_ids']
     search_fields = ['video_title']
     list_filter = ['active']
-    readonly_fields = ['id', 'is_published']
+    readonly_fields = ['id', 'is_published', 'publish_timestamp', 'get_playlist_ids']
     class Meta:
         model = VideoAllProxy
 admin.site.register(VideoAllProxy, VideoAllAdmin)
diff --git a/videos/models.py b/videos/models.py
index 731ea73..213933f 100644
--- a/videos/models.py
+++ b/videos/models.py
@@ -1,12 +1,37 @@
 from django.db import models
-from django.db.models.fields import proxy
-from django.test.testcases import TestCase
+# from django.db.models.fields import proxy
+# from django.test.testcases import TestCase
 from django.utils import timezone
 from django.utils.text import slugify
+from django.db.models.signals import pre_save
+from netflix.db.models import PublishStateOptions
+from netflix.db.recievers import publish_state_pre_save, slugify_pre_save
+
+# video.objects.sorted() => manager method
+# video.objects.all.sorted() => queryset method
+# default manager => objects (objects or items = models.Manager())
+# after this have to do => video.items.all() not objects.all()
+# create a own manager that inherits from default manager
+# then have to craete a method
+# also default queryset does not has sorted method
+# inside manager, define get queryset method inherting from previous queryset  
+# then create a class for queryset and define the functionality
+
+class VideoQuerySet(models.QuerySet):
+    def published(self):
+        now = timezone.now()
+        return self.filter(state=PublishStateOptions.PUBLISH, publish_timestamp__lte = now)
+class VideoManager(models.Manager):
+    def get_queryset(self):
+        return VideoQuerySet(self.model, using=self.__db)
+
+    def published(self):
+        return self.get_queryset().published()
+
 class Video(models.Model):
-    class VideoStateOptions(models.TextChoices):
-        PUBLISH = 'PU', 'Pubish'
-        DRAFT = 'DR', 'Draft'
+    # class VideoStateOptions(models.TextChoices):
+    #     PUBLISH = 'PU', 'Pubish'
+    #     DRAFT = 'DR', 'Draft'
 
     video_title = models.CharField(max_length=400)
     description = models.TextField(blank=True)
@@ -17,8 +42,8 @@ class Video(models.Model):
     updated = models.DateTimeField(auto_now_add=True)
     state  = models.CharField(
                 max_length=2,
-                choices=VideoStateOptions.choices,
-                default = VideoStateOptions.DRAFT)
+                choices=PublishStateOptions.choices,
+                default = PublishStateOptions.DRAFT)
 
     publish_timestamp = models.DateTimeField(
                 auto_now_add=False,
@@ -28,21 +53,25 @@ class Video(models.Model):
 
     def __str__(self):
         return self.video_title
+    objects = VideoManager()
 
     @property
     def is_published(self):
         return self.active
 
-    def save(self, *args, **kwargs):
-        if self.state == self.VideoStateOptions.PUBLISH and self.publish_timestamp is None:
-            print("Save as timestamp for published")
-            self.publish_timestamp = timezone.now()
-        elif self.state == self.VideoStateOptions.DRAFT:
-            self.publish_timestamp = None
+    def get_playlist_ids(self):
+        return list(self.playlist_set.all().values_list('id', flat=True))
+
+    # def save(self, *args, **kwargs):
+    #     if self.state == self.VideoStateOptions.PUBLISH and self.publish_timestamp is None:
+    #         print("Save as timestamp for published")
+    #         self.publish_timestamp = timezone.now()
+    #     elif self.state == self.VideoStateOptions.DRAFT:
+    #         self.publish_timestamp = None
 
-        if self.slug is None:
-            self.slug = slugify(self.video_title)
-        super.save(*args, **kwargs)
+    #     if self.slug is None:
+    #         self.slug = slugify(self.video_title)
+    #     super.save(*args, **kwargs)
 
 
 # Proxy Model
@@ -56,3 +85,7 @@ class VideoPublishedProxy(Video):
     class Meta:
         proxy = True
         verbose_name = 'Published Video'
+
+# calling django signals
+pre_save.connect(publish_state_pre_save, sender=Video)
+pre_save.connect(slugify_pre_save, sender=Video)
\ No newline at end of file
diff --git a/videos/tests.py b/videos/tests.py
index 9d68590..0e462ce 100644
--- a/videos/tests.py
+++ b/videos/tests.py
@@ -1,42 +1,42 @@
-from django.test import TestCase
-from django.utils import timezone
+# from django.test import TestCase
+# from django.utils import timezone
 
-from .models import Video
+# from .models import Video
 
-# class VideoModelTestCase(TestCase):
-#     def setUp(self):
-#         Video.objects.create(video_title="Interstellar")
+# # class VideoModelTestCase(TestCase):
+# #     def setUp(self):
+# #         Video.objects.create(video_title="Interstellar")
     
-#     def test_valid_title(self):
-#         title = "Interstellar"
-#         qs = Video.objects.filter(video_title=title)
-#         self.assertTrue(qs.exists())
-
-#     def test_created_count(self):
-#         qs = Video.objects.all()
-#         self.assertEqual(qs.count(), 1)
-
-class VideoModeltestCase(TestCase):
-    def setUp(self):
-        Video.objects.create(video_title='Star Wars')
-        Video.objects.create(video_title="Star Wart", state=Video.VideoStateOptions.PUBLISH)
-
-        def test_valid_title(self):
-            title = 'Star Wart'
-
-        def test_createed_count(self):
-            qs = Video.objects.all()
-            self.assertEqual(qs.count(), 2)
-
-        def test_draft_case(self):
-            qs = Video.objects.filter(state=Video.VideoStateOptions.DRAFT)
-            self.assertEqual(qs.count(), 1)
-
-        def test_publish_case(self):
-            qs = Video.objects.filter(state=Video.VideoStateOptions.PUBLISH)
-            now = timezone.now()
-            published_qs = Video.objects.filter(
-                            state=Video.VideoStateOptions.PUBLISH,
-                            publish_timestamp__lte=now
-            )
-            self.assertTrue(published_qs.exists()) 
\ No newline at end of file
+# #     def test_valid_title(self):
+# #         title = "Interstellar"
+# #         qs = Video.objects.filter(video_title=title)
+# #         self.assertTrue(qs.exists())
+
+# #     def test_created_count(self):
+# #         qs = Video.objects.all()
+# #         self.assertEqual(qs.count(), 1)
+
+# class VideoModeltestCase(TestCase):
+#     def setUp(self):
+#         Video.objects.create(video_title='Star Wars')
+#         Video.objects.create(video_title="Star Wart", state=Video.VideoStateOptions.PUBLISH)
+
+#         def test_valid_title(self):
+#             title = 'Star Wart'
+
+#         def test_createed_count(self):
+#             qs = Video.objects.all()
+#             self.assertEqual(qs.count(), 2)
+
+#         def test_draft_case(self):
+#             qs = Video.objects.filter(state=Video.VideoStateOptions.DRAFT)
+#             self.assertEqual(qs.count(), 1)
+
+#         def test_publish_case(self):
+#             qs = Video.objects.filter(state=Video.VideoStateOptions.PUBLISH)
+#             now = timezone.now()
+#             published_qs = Video.objects.filter(
+#                             state=Video.VideoStateOptions.PUBLISH,
+#                             publish_timestamp__lte=now
+#             )
+#             self.assertTrue(published_qs.exists()) 
\ No newline at end of file
