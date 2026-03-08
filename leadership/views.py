from django.shortcuts import render, get_object_or_404
from .models import OfficeBearer, ManagementPost

def index(request):
    """Display all current office bearers"""
    current_bearers = OfficeBearer.objects.filter(status='current').select_related('post').order_by('post__priority')
    posts = ManagementPost.objects.filter(is_active=True).order_by('priority')
    
    context = {
        'current_bearers': current_bearers,
        'posts': posts,
    }
    return render(request, 'leadership/index.html', context)

def bearer_detail(request, slug):
    """Display individual office bearer details"""
    bearer = get_object_or_404(OfficeBearer, slug=slug, status='current')
    context = {
        'bearer': bearer,
    }
    return render(request, 'leadership/bearer_detail.html', context)
