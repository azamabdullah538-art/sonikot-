from django.shortcuts import render, get_object_or_404
from .models import WelfareProgram, ProgramCategory

def index(request):
    """
    Display all active welfare programs organized by categories.
    """
    # Get active categories with their programs
    categories = ProgramCategory.objects.filter(
        is_active=True
    ).prefetch_related('programs').order_by('priority', 'name')
    
    # Get featured programs
    featured_programs = WelfareProgram.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related('category')[:6]  # Limit to 6 featured programs
    
    context = {
        'categories': categories,
        'featured_programs': featured_programs,
    }
    
    return render(request, 'programs/index.html', context)

def program_detail(request, slug):
    """
    Display detailed view of a specific welfare program.
    """
    program = get_object_or_404(
        WelfareProgram.objects.select_related('category'),
        slug=slug,
        is_active=True
    )
    
    # Get related programs from same category
    related_programs = WelfareProgram.objects.filter(
        category=program.category,
        is_active=True
    ).exclude(id=program.id)[:3]
    
    context = {
        'program': program,
        'related_programs': related_programs,
    }
    
    return render(request, 'programs/program_detail.html', context)
