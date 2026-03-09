from django.shortcuts import render, get_object_or_404
from .models import Program, ProgramCategory

def program_list(request):
    """Display list of all programs."""
    programs = Program.objects.filter(is_active=True).order_by('-created_at')
    categories = ProgramCategory.objects.all()
    
    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        programs = programs.filter(category__slug=category_slug)
    
    context = {
        'programs': programs,
        'categories': categories,
    }
    return render(request, 'programs/index.html', context)

def program_detail(request, slug):
    """Display detail view of a specific program."""
    program = get_object_or_404(Program, slug=slug, is_active=True)
    context = {
        'program': program,
    }
    return render(request, 'programs/program_detail.html', context)
