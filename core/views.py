 

# Create your views here.
from django.shortcuts import render
from .models import Testimonial, GalleryImage, SiteSettings
from leadership.models import OfficeBearer

def home(request):
    """Home page view with featured content"""
    # Get featured testimonials
    testimonials = Testimonial.objects.filter(is_active=True, is_featured=True)[:3]

    # Get featured gallery images
    gallery_images = GalleryImage.objects.filter(is_active=True, is_featured=True)[:6]

    # Get current office bearers
    leaders = OfficeBearer.objects.filter(status='current').order_by('post__priority')

    context = {
        'testimonials': testimonials,
        'gallery_images': gallery_images,
        'leaders': leaders,
    }
    return render(request, 'core/home.html', context)

def about(request):
    """About page view"""
    # Get site settings for about content
    site_settings = SiteSettings.objects.first()

    # Get all testimonials for about page
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')[:6]

    context = {
        'site_settings': site_settings,
        'testimonials': testimonials,
    }
    return render(request, 'core/about.html', context)

def contact(request):
    """Contact page view"""
    site_settings = SiteSettings.objects.first()

    if request.method == 'POST':
        from .models import ContactSubmission
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Create contact submission
        ContactSubmission.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )

        # Here you could add email sending logic
        # For now, just show success message
        from django.contrib import messages
        messages.success(request, 'Thank you for your message! We will get back to you soon.')

        # Redirect to avoid form resubmission
        from django.shortcuts import redirect
        return redirect('core:contact')

    context = {
        'site_settings': site_settings,
    }
    return render(request, 'core/contact.html', context)

def gallery(request):
    """Gallery page view"""
    # Get all active gallery images organized by category
    from .models import GalleryCategory
    categories = GalleryCategory.objects.filter(is_active=True).prefetch_related('images').order_by('priority', 'name')

    context = {
        'categories': categories,
    }
    return render(request, 'core/gallery.html', context)
