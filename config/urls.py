"""
URL configuration for Sonikot Youth Welfear Foundation project.

Professional routing with proper namespacing and media file handling.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # Core app (home, about, contact)
    path('', include('core.urls', namespace='core')),
    
    # Leadership app
    path('leadership/', include('leadership.urls', namespace='leadership')),
    
    # Programs app
    path('programs/', include('programs.urls', namespace='programs')),

    # Donations app
    path('donations/', include('donations.urls', namespace='donations')),

    # Phase 2: Volunteers (commented for now)
    # path('volunteers/', include('volunteers.urls', namespace='volunteers')),
]

# Customize admin panel
admin.site.site_header = "Sonikot Youth Welfear Foundation Admin"
admin.site.site_title = "SYWO Admin Portal"
admin.site.index_title = "Welcome to SYWO Administration"

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
