from django.contrib import admin
from django.utils.html import format_html

from .models import *


@admin.register(CollaborationProject)
class CollaborationProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_request_status', 'created_at', 'participants_list')
    list_filter = ('created_at', 'request__status')  # Simple filter syntax
    search_fields = ('title', 'request__title', 'participants__username')
    raw_id_fields = ('request',)
    filter_horizontal = ('participants',)

    def get_request_status(self, obj):
        return obj.request.status if obj.request else '-'

    get_request_status.short_description = 'Request Status'
    get_request_status.admin_order_field = 'request__status'

    def participants_list(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])

    participants_list.short_description = 'Participants'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('request')


@admin.register(CollaborationMessage)
class CollaborationMessageAdmin(admin.ModelAdmin):
    list_display = ('truncated_content', 'project', 'sender', 'timestamp')
    search_fields = ('content', 'project__title', 'sender__username')
    list_filter = ('project', 'sender', 'timestamp')
    raw_id_fields = ('project', 'sender')

    def truncated_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    truncated_content.short_description = 'Content'


@admin.register(SharedFile)
class SharedFileAdmin(admin.ModelAdmin):
    list_display = ('get_filename', 'project', 'uploaded_by', 'uploaded_at')
    search_fields = ('file', 'project__title', 'uploaded_by__username')
    list_filter = ('project', 'uploaded_by', 'uploaded_at')
    raw_id_fields = ('project', 'uploaded_by')

    def get_filename(self, obj):
        return obj.file.name.split('/')[-1]

    get_filename.short_description = 'Filename'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'formatted_due_date', 'assigned_to')
    search_fields = ('title', 'project__title', 'assigned_to__username')
    list_filter = ('status', 'due_date', 'project')
    raw_id_fields = ('project', 'assigned_to')

    def formatted_due_date(self, obj):
        return obj.due_date.strftime("%b %d, %Y")

    formatted_due_date.short_description = 'Due Date'

    def status_style(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            '#00ff88' if obj.status == 'done' else '#ff4d4d' if obj.status == 'todo' else '#ee10b0',
            obj.get_status_display()
        )

    status_style.short_description = 'Status'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'truncated_message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
    readonly_fields = ('created_at',)

    def truncated_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message

    truncated_message.short_description = 'Message'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'bio', 'profile_picture')  # Display role
    search_fields = ('user__username', 'role')  # Allow searching by username or role
    list_filter = ('role',)  # Filter by roles, e.g., musician, listener


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date')
    search_fields = ('title', 'artist')
    list_filter = ('release_date',)
    ordering = ('release_date',)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'profile_url')
    search_fields = ('name', 'genre')
    list_filter = ('genre',)
    ordering = ('name',)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "release_date", "album", "duration", "genre", "created_at", "play_count")
    list_filter = ("artist", "album", "release_date")
    search_fields = ("title", "artist__name", "album__title", "genre__name")
    ordering = ('release_date',)


@admin.register(LikedSong)
class LikedTracksAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'liked_at')
    search_fields = ('user__username', 'track__title')
    list_filter = ('liked_at',)
    ordering = ('liked_at',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('preferences',)
    search_fields = ('user__username',)
    ordering = ('user',)


@admin.register(CollaborationRequest)
class CollaborationRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'sender', 'receiver', 'status', 'created_at')
    search_fields = ('title', 'sender__username', 'receiver__username')
    list_filter = ('status',)

    actions = ['accept_requests', 'decline_requests']

    def accept_requests(self, request, queryset):
        queryset.update(status='accepted')
        self.message_user(request, "Selected requests have been accepted.")

    def decline_requests(self, request, queryset):
        queryset.update(status='declined')
        self.message_user(request, "Selected requests have been declined.")


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')  # Display name, user, and creation date
    search_fields = ('name', 'user__username')  # Allow searching by playlist name and user
    list_filter = ('user', 'created_at')  # Filter by user and creation date
    ordering = ('created_at',)  # Order by creation date


# Customizing the admin site header
admin.site.site_header = "Artist Management Admin"
admin.site.site_title = "Artist Admin Portal"
admin.site.index_title = "Welcome to the Artist Management Dashboard"
