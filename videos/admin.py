from typing import ValuesView
from django.contrib import admin
from django.contrib.admin.decorators import action

from .models import VideoAllProxy, VideoPublishedProxy

# class VideoAllAdmin(admin.ModelAdmin):
#     list_display = ['video_title', 'video_id']
#     search_fields = ['video_title']
    
#     class Meta:
#         model = VideoAllProxy

# admin.site.register(VideoAllProxy, VideoAllAdmin)
class VideoAllAdmin(admin.ModelAdmin):
    list_display = ['video_title', 'video_id']
    search_fields = ['video_title']
    # list_filter = ['video_id']
    class Meta:
        model = VideoAllProxy
admin.site.register(VideoAllProxy, VideoAllAdmin)

# class VideoPublishedProxyAdmin(admin.ModelAdmin):
#     list_display = ['video_title', 'video_id']
#     search_fields = ['title']
#     class Meta:
#         model = VideoPublishedProxy

#     def get_queryset(self, request):
#         return VideoAllProxy.objects.filter(active=True)

# admin.site.register(VideoPublishedProxy, VideoPublishedProxyAdmin)

class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ['video_title', 'video_id']
    search_fields = ['video_title']
    class Meta:
        model = VideoPublishedProxy

    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(active=True)


admin.site.register(VideoPublishedProxy, VideoPublishedProxyAdmin)