from django.contrib import admin
from .models import Program, ProgramCategory

@admin.register(ProgramCategory)
class ProgramCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'start_date', 'end_date', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'short_description', 'description']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
