"""
Context Processors - Sonikot Youth Welfear Foundation

Makes organization information and site settings available in all templates.
"""

from django.conf import settings


def organization_info(request):
    """
    Add organization information to all template contexts.
    This makes ORGANIZATION settings available in every template.
    """
    try:
        from core.models import SiteSettings, Testimonial, GalleryImage

        # Get site settings (creates if doesn't exist)
        site_settings = SiteSettings.load()

        # Get featured testimonials
        testimonials = Testimonial.objects.filter(is_active=True, is_featured=True)[:3]

        # Get featured gallery images
        gallery_images = GalleryImage.objects.filter(is_active=True, is_featured=True)[:6]
    except Exception as e:
        # Fallback if database is not ready or models not migrated
        site_settings = None
        testimonials = []
        gallery_images = []

    return {
        'organization': settings.ORGANIZATION,  # lowercase for template consistency
        'ORGANIZATION': settings.ORGANIZATION,  # uppercase for backward compatibility
        'site_settings': site_settings,
        'testimonials': testimonials,
        'gallery_images': gallery_images,
        'current_year': __import__('datetime').datetime.now().year,
    }
