from typing import ValuesView
from django.contrib import admin
from django.contrib.admin.decorators import action
from django.utils import timezone
from .models import VideoAllProxy, VideoPublishedProxy

class VideoAllAdmin(admin.ModelAdmin):
    list_display = ['video_title', 'id', 'video_id', 'is_published']
    search_fields = ['video_title']
    list_filter = ['active']
    readonly_fields = ['id', 'is_published']
    class Meta:
        model = VideoAllProxy
admin.site.register(VideoAllProxy, VideoAllAdmin)

class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ['video_title', 'video_id']
    search_fields = ['video_title']
    class Meta:
        model = VideoPublishedProxy

    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(active=True)


admin.site.register(VideoPublishedProxy, VideoPublishedProxyAdmin)
