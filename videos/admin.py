from django.contrib import admin

from .models import (
        VideoAllProxy,
        VideoPublishedProxy
)

# Admin register for all videos proxy
class VideoAllAdmin(admin.ModelAdmin):        ###
        list_display = ['title', 'id', 'state', 'video_id', 'is_published']
        search_fields = ['titile']
        list_filter = ['state', 'active']
        readonly_fields = ['id', 'is_published', 'publish_timestamp']    ###

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
                return VideoAllProxy.objects.filter(active=True)

admin.site.register(VideoPublishedProxy, VideoPublishedProxyAdmin)

