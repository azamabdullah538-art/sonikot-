"""
Admin Configuration - Core App

Professional admin interface for core functionality.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ContactSubmission, GalleryCategory, GalleryImage,
    Testimonial, SiteSettings
)


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    """Admin for contact form submissions"""
    list_display = ['full_name', 'email', 'subject', 'status_badge', 'submitted_at']
    list_filter = ['status', 'subject', 'submitted_at']
    search_fields = ['full_name', 'email', 'message']
    readonly_fields = ['full_name', 'email', 'phone', 'subject', 'message',
                       'ip_address', 'user_agent', 'submitted_at']
    date_hierarchy = 'submitted_at'
    actions = ['mark_as_read', 'mark_as_replied']
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Management', {
            'fields': ('status', 'admin_notes')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent', 'submitted_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'new': '#dc3545',
            'read': '#ffc107',
            'replied': '#007bff',
            'resolved': '#28a745'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(status='read')
        self.message_user(request, f'{updated} submission(s) marked as read.')
    mark_as_read.short_description = "Mark as Read"
    
    def mark_as_replied(self, request, queryset):
        updated = queryset.update(status='replied')
        self.message_user(request, f'{updated} submission(s) marked as replied.')
    mark_as_replied.short_description = "Mark as Replied"


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    """Admin for gallery categories"""
    list_display = ['name', 'priority', 'image_count', 'is_active', 'created_at']
    list_editable = ['priority', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    
    def image_count(self, obj):
        count = obj.images.filter(is_active=True).count()
        return format_html('<strong>{}</strong>', count)
    image_count.short_description = 'Images'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    """Admin for gallery images"""
    list_display = ['image_thumbnail', 'title', 'category', 'event_date', 'is_featured', 'is_active', 'uploaded_at']
    list_filter = ['category', 'is_featured', 'is_active', 'event_date']
    search_fields = ['title', 'description', 'location']
    list_editable = ['is_featured', 'is_active']
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Image Information', {
            'fields': ('category', 'title', 'image', 'description')
        }),
        ('Event Details', {
            'fields': ('event_date', 'location', 'photographer')
        }),
        ('Visibility', {
            'fields': ('is_featured', 'is_active')
        }),
    )
    
    def image_thumbnail(self, obj):
        return format_html(
            '<img src="{}" style="width: 80px; height: 50px; object-fit: cover; border-radius: 5px;" />',
            obj.image.url
        )
    image_thumbnail.short_description = 'Image'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Admin for testimonials"""
    list_display = ['photo_thumbnail', 'full_name', 'role', 'rating_display', 'is_featured', 'is_active', 'created_at']
    list_filter = ['rating', 'is_featured', 'is_active']
    search_fields = ['full_name', 'role', 'testimonial']
    list_editable = ['is_featured', 'is_active']
    
    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />',
                obj.photo.url
            )
        return format_html('<span style="color: #999;">No Photo</span>')
    photo_thumbnail.short_description = 'Photo'
    
    def rating_display(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: #ffc107; font-size: 16px;">{}</span>', stars)
    rating_display.short_description = 'Rating'


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin for site settings - single instance only"""
    
    fieldsets = (
        ('About Organization', {
            'fields': ('mission', 'vision', 'values', 'history')
        }),
        ('Homepage Hero Section', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_image')
        }),
        ('Statistics', {
            'fields': ('total_beneficiaries', 'active_programs', 'volunteers_count', 'years_of_service')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url', 'linkedin_url', 'whatsapp_number')
        }),
        ('Footer', {
            'fields': ('footer_text',)
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent adding more than one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deleting the settings
        return False