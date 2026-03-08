"""
Admin Configuration - Programs App

Professional admin interface for managing welfare programs.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import ProgramCategory, WelfareProgram, ProgramImage, ProgramUpdate


@admin.register(ProgramCategory)
class ProgramCategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for program categories.
    """
    list_display = ['name', 'color_display', 'priority', 'program_count', 'is_active', 'created_at']
    list_editable = ['priority', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['priority', 'name']
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'description', 'icon', 'color', 'priority')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def color_display(self, obj):
        """Display color with preview"""
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 15px; border-radius: 3px;">{}</span>',
            obj.color,
            obj.color
        )
    color_display.short_description = 'Color'
    
    def program_count(self, obj):
        """Display count of programs in this category"""
        count = obj.programs.filter(is_active=True).count()
        return format_html(
            '<span style="font-weight: bold;">{} active</span>',
            count
        )
    program_count.short_description = 'Programs'


class ProgramImageInline(admin.TabularInline):
    """
    Inline admin for program images.
    """
    model = ProgramImage
    extra = 1
    fields = ['image', 'caption', 'priority']
    ordering = ['priority']


class ProgramUpdateInline(admin.StackedInline):
    """
    Inline admin for program updates.
    """
    model = ProgramUpdate
    extra = 0
    fields = ['title', 'description', 'image', 'update_date']
    ordering = ['-update_date']


@admin.register(WelfareProgram)
class WelfareProgramAdmin(admin.ModelAdmin):
    """
    Admin interface for welfare programs.
    """
    list_display = [
        'featured_image_thumbnail',
        'title',
        'category',
        'status_badge',
        'budget_info',
        'impact_info',
        'is_featured',
        'is_active',
        'created_at'
    ]
    list_filter = ['status', 'category', 'is_featured', 'is_active', 'start_date', 'created_at']
    search_fields = ['title', 'short_description', 'detailed_description', 'location']
    readonly_fields = ['slug', 'featured_image_preview', 'created_at', 'updated_at']
    date_hierarchy = 'start_date'
    list_editable = ['is_featured', 'is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'short_description')
        }),
        ('Detailed Description', {
            'fields': ('detailed_description', 'objectives'),
        }),
        ('Media', {
            'fields': ('featured_image', 'featured_image_preview'),
        }),
        ('Status & Timeline', {
            'fields': ('status', 'start_date', 'end_date'),
        }),
        ('Budget & Resources', {
            'fields': ('estimated_budget', 'actual_cost'),
            'classes': ('collapse',)
        }),
        ('Impact Metrics', {
            'fields': ('target_beneficiaries', 'actual_beneficiaries'),
            'classes': ('collapse',)
        }),
        ('Location & Visibility', {
            'fields': ('location', 'is_active', 'is_featured'),
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ProgramImageInline, ProgramUpdateInline]
    
    actions = ['mark_as_completed', 'mark_as_ongoing', 'mark_as_featured']
    
    def featured_image_thumbnail(self, obj):
        """Display small image thumbnail"""
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                obj.featured_image.url
            )
        return format_html('<span style="color: #999;">No Image</span>')
    featured_image_thumbnail.short_description = 'Image'
    
    def featured_image_preview(self, obj):
        """Display larger image preview"""
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-width: 500px; max-height: 300px; border-radius: 10px;" />',
                obj.featured_image.url
            )
        return format_html('<span style="color: #999;">No image uploaded</span>')
    featured_image_preview.short_description = 'Image Preview'
    
    def status_badge(self, obj):
        """Display colored status badge"""
        colors = {
            'planning': '#6c757d',
            'ongoing': '#007bff',
            'completed': '#28a745',
            'on_hold': '#ffc107',
            'cancelled': '#dc3545'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    def budget_info(self, obj):
        """Display budget information"""
        if obj.estimated_budget:
            actual = obj.actual_cost or 0
            percentage = obj.budget_spent_percentage or 0
            
            color = '#28a745' if percentage <= 100 else '#dc3545'
            
            return format_html(
                '<strong>Est:</strong> Rs. {:,.0f}<br>'
                '<strong>Act:</strong> Rs. {:,.0f}<br>'
                '<small style="color: {};">{}% spent</small>',
                obj.estimated_budget,
                actual,
                color,
                percentage
            )
        return format_html('<span style="color: #999;">Not set</span>')
    budget_info.short_description = 'Budget'
    
    def impact_info(self, obj):
        """Display impact metrics"""
        if obj.target_beneficiaries:
            actual = obj.actual_beneficiaries or 0
            percentage = obj.beneficiary_reach_percentage or 0
            
            color = '#28a745' if percentage >= 80 else '#ffc107'
            
            return format_html(
                '<strong>Target:</strong> {:,}<br>'
                '<strong>Reached:</strong> {:,}<br>'
                '<small style="color: {};">{}% reached</small>',
                obj.target_beneficiaries,
                actual,
                color,
                percentage
            )
        return format_html('<span style="color: #999;">Not set</span>')
    impact_info.short_description = 'Impact'
    
    def mark_as_completed(self, request, queryset):
        """Mark selected programs as completed"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} program(s) marked as completed.')
    mark_as_completed.short_description = "Mark as Completed"
    
    def mark_as_ongoing(self, request, queryset):
        """Mark selected programs as ongoing"""
        updated = queryset.update(status='ongoing')
        self.message_user(request, f'{updated} program(s) marked as ongoing.')
    mark_as_ongoing.short_description = "Mark as Ongoing"
    
    def mark_as_featured(self, request, queryset):
        """Mark selected programs as featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} program(s) marked as featured.')
    mark_as_featured.short_description = "Mark as Featured"


@admin.register(ProgramImage)
class ProgramImageAdmin(admin.ModelAdmin):
    """
    Admin interface for program images.
    """
    list_display = ['image_thumbnail', 'program', 'caption', 'priority', 'uploaded_at']
    list_filter = ['program', 'uploaded_at']
    search_fields = ['program__title', 'caption']
    list_editable = ['priority']
    ordering = ['program', 'priority', '-uploaded_at']
    
    def image_thumbnail(self, obj):
        """Display image thumbnail"""
        return format_html(
            '<img src="{}" style="width: 80px; height: 50px; object-fit: cover; border-radius: 5px;" />',
            obj.image.url
        )
    image_thumbnail.short_description = 'Image'


@admin.register(ProgramUpdate)
class ProgramUpdateAdmin(admin.ModelAdmin):
    """
    Admin interface for program updates.
    """
    list_display = ['program', 'title', 'update_date', 'has_image', 'created_at']
    list_filter = ['program', 'update_date', 'created_at']
    search_fields = ['program__title', 'title', 'description']
    date_hierarchy = 'update_date'
    ordering = ['-update_date']
    
    fieldsets = (
        ('Update Information', {
            'fields': ('program', 'title', 'description', 'update_date')
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )
    
    def has_image(self, obj):
        """Check if update has an image"""
        if obj.image:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: #ccc;">✗</span>')
    has_image.short_description = 'Image'
