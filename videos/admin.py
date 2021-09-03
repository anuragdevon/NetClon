from django.contrib import admin

from .models import (
        Video,
        VideoAllProxy,
        VideoPublishedProxy
)
admin.site.register(Video)
admin.site.register(VideoPublishedProxy)

# Admin register for all videos proxy
class VideoAllAdmin(admin.ModelAdmin):        ###
        list_display = ['title', 'video_id']
        search_fields = ['titile']

        class Meta:
                model = VideoAllProxy

admin.site.register(VideoAllProxy, VideoAllAdmin)

# Admin register for all published video proxy
class VideoPublishedProxyAdmin(admin.ModelAdmin):
        list_display = ['title', 'video_id']
        search_fields = ['title']
        class Meta:
                model = VideoPublishedProxy

        def get_queryset(self, request):        ###
                return VideoProxy.objects.filter(active=True)

admin.site.register(VideoPublishedProxy, VideoPublishedProxyAdmin)

