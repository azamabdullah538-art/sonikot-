"""
Admin Configuration - Leadership App

Professional admin interface for managing leadership and office bearers.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import ManagementPost, OfficeBearer, LeadershipHistory


@admin.register(ManagementPost)
class ManagementPostAdmin(admin.ModelAdmin):
    """
    Admin interface for managing leadership positions.
    """
    list_display = ['title', 'priority', 'is_active', 'current_holders_count', 'created_at']
    list_editable = ['priority', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['priority', 'title']
    
    fieldsets = (
        ('Position Information', {
            'fields': ('title', 'description', 'priority')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def current_holders_count(self, obj):
        """Display count of current office bearers in this position"""
        count = obj.office_bearers.filter(status='current').count()
        color = 'green' if count > 0 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            count
        )
    current_holders_count.short_description = 'Current Holders'


class LeadershipHistoryInline(admin.TabularInline):
    """
    Inline admin for leadership history.
    """
    model = LeadershipHistory
    extra = 0
    fields = ['event_type', 'event_date', 'description']
    ordering = ['-event_date']


@admin.register(OfficeBearer)
class OfficeBearerAdmin(admin.ModelAdmin):
    """
    Admin interface for managing office bearers.
    """
    list_display = [
        'photo_thumbnail',
        'full_name',
        'post',
        'status_badge',
        'term_info',
        'contact_info',
        'created_at'
    ]
    list_filter = ['status', 'post', 'term_start', 'created_at']
    search_fields = ['full_name', 'email', 'phone', 'bio']
    readonly_fields = ['slug', 'photo_preview', 'created_at', 'updated_at']
    date_hierarchy = 'term_start'
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'photo', 'photo_preview', 'bio')
        }),
        ('Position Details', {
            'fields': ('post', 'status', 'term_start', 'term_end')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone'),
            'classes': ('collapse',)
        }),
        ('URL & Metadata', {
            'fields': ('slug', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [LeadershipHistoryInline]
    
    actions = ['mark_as_former', 'mark_as_current']
    
    def photo_thumbnail(self, obj):
        """Display small photo thumbnail in list view"""
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />',
                obj.photo.url
            )
        return format_html('<span style="color: #999;">No Photo</span>')
    photo_thumbnail.short_description = 'Photo'
    
    def photo_preview(self, obj):
        """Display larger photo preview in detail view"""
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 10px;" />',
                obj.photo.url
            )
        return format_html('<span style="color: #999;">No photo uploaded</span>')
    photo_preview.short_description = 'Photo Preview'
    
    def status_badge(self, obj):
        """Display colored status badge"""
        colors = {
            'current': '#28a745',
            'former': '#6c757d'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    def term_info(self, obj):
        """Display term duration information"""
        if obj.term_end:
            duration = obj.term_duration
            return format_html(
                '{} to {}<br><small style="color: #666;">({} years)</small>',
                obj.term_start.strftime('%b %Y'),
                obj.term_end.strftime('%b %Y'),
                duration
            )
        return format_html(
            '{} - Present<br><small style="color: #28a745;">Ongoing</small>',
            obj.term_start.strftime('%b %Y')
        )
    term_info.short_description = 'Term'
    
    def contact_info(self, obj):
        """Display contact information"""
        info = []
        if obj.email:
            info.append(format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email))
        if obj.phone:
            info.append(format_html('<a href="tel:{}">{}</a>', obj.phone, obj.phone))
        return format_html('<br>'.join(info)) if info else format_html('<span style="color: #999;">No contact</span>')
    contact_info.short_description = 'Contact'
    
    def mark_as_former(self, request, queryset):
        """Bulk action to mark selected office bearers as former"""
        updated = queryset.update(status='former')
        self.message_user(request, f'{updated} office bearer(s) marked as former.')
    mark_as_former.short_description = "Mark selected as Former"
    
    def mark_as_current(self, request, queryset):
        """Bulk action to mark selected office bearers as current"""
        updated = queryset.update(status='current')
        self.message_user(request, f'{updated} office bearer(s) marked as current.')
    mark_as_current.short_description = "Mark selected as Current"
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }


@admin.register(LeadershipHistory)
class LeadershipHistoryAdmin(admin.ModelAdmin):
    """
    Admin interface for leadership history records.
    """
    list_display = ['office_bearer', 'event_type', 'event_date', 'created_at']
    list_filter = ['event_type', 'event_date', 'created_at']
    search_fields = ['office_bearer__full_name', 'description']
    date_hierarchy = 'event_date'
    ordering = ['-event_date']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('office_bearer', 'event_type', 'event_date')
        }),
        ('Details', {
            'fields': ('description',)
        }),
    )
