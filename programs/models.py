"""
Programs Models - Sonikot Youth Welfear Foundation

Professional database models for managing welfare programs.
"""

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator


class ProgramCategory(models.Model):
    """
    Categories for organizing welfare programs.
    Examples: Education, Health, Emergency Relief, Community Development
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Category name (e.g., Education, Health, Emergency Relief)"
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon class name (e.g., fa-graduation-cap for Font Awesome)"
    )
    description = models.TextField(
        blank=True,
        help_text="Brief description of this category"
    )
    color = models.CharField(
        max_length=7,
        default='#007bff',
        help_text="Hex color code for UI display (e.g., #007bff)"
    )
    priority = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower number = higher priority)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Is this category active?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['priority', 'name']
        verbose_name = "Program Category"
        verbose_name_plural = "Program Categories"
    
    def __str__(self):
        return self.name
    
    @property
    def active_programs_count(self):
        """Count of active programs in this category"""
        return self.programs.filter(is_active=True).count()


class WelfareProgram(models.Model):
    """
    Represents individual welfare programs/projects.
    Tracks program details, status, budget, and impact.
    """
    
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Basic Information
    title = models.CharField(
        max_length=200,
        help_text="Program title"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        help_text="Auto-generated URL slug"
    )
    category = models.ForeignKey(
        ProgramCategory,
        on_delete=models.PROTECT,
        related_name='programs',
        help_text="Program category"
    )
    
    # Description
    short_description = models.CharField(
        max_length=300,
        help_text="Brief summary (shown in listings)"
    )
    detailed_description = models.TextField(
        help_text="Detailed program description"
    )
    objectives = models.TextField(
        blank=True,
        help_text="Program objectives and goals"
    )
    
    # Media
    featured_image = models.ImageField(
        upload_to='programs/featured/%Y/',
        blank=True,
        null=True,
        help_text="Main program image (recommended: 1200x600px)"
    )
    
    # Status and Timeline
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planning',
        help_text="Current program status"
    )
    start_date = models.DateField(
        blank=True,
        null=True,
        help_text="Program start date"
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        help_text="Program end date (if applicable)"
    )
    
    # Budget and Resources
    estimated_budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="Estimated budget in PKR"
    )
    actual_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="Actual cost incurred in PKR"
    )
    
    # Impact Metrics
    target_beneficiaries = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Estimated number of beneficiaries"
    )
    actual_beneficiaries = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Actual number of people helped"
    )
    
    # Location
    location = models.CharField(
        max_length=200,
        blank=True,
        help_text="Program location (e.g., Sonikot, Gilgit)"
    )
    
    # Visibility
    is_active = models.BooleanField(
        default=True,
        help_text="Show this program on website?"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Feature this program on homepage?"
    )
    
    # SEO
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="SEO meta description"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = "Welfare Program"
        verbose_name_plural = "Welfare Programs"
        indexes = [
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not provided"""
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while WelfareProgram.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        # Auto-generate meta description from short description
        if not self.meta_description and self.short_description:
            self.meta_description = self.short_description[:160]
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Get URL for program detail page"""
        return reverse('programs:program_detail', kwargs={'slug': self.slug})
    
    @property
    def is_ongoing(self):
        """Check if program is currently ongoing"""
        return self.status == 'ongoing'
    
    @property
    def is_completed(self):
        """Check if program is completed"""
        return self.status == 'completed'
    
    @property
    def budget_spent_percentage(self):
        """Calculate percentage of budget spent"""
        if self.estimated_budget and self.actual_cost:
            return round((self.actual_cost / self.estimated_budget) * 100, 1)
        return None
    
    @property
    def beneficiary_reach_percentage(self):
        """Calculate percentage of target beneficiaries reached"""
        if self.target_beneficiaries and self.actual_beneficiaries:
            return round((self.actual_beneficiaries / self.target_beneficiaries) * 100, 1)
        return None


class ProgramImage(models.Model):
    """
    Additional images for welfare programs (gallery).
    """
    
    program = models.ForeignKey(
        WelfareProgram,
        on_delete=models.CASCADE,
        related_name='images',
        help_text="Related program"
    )
    image = models.ImageField(
        upload_to='programs/gallery/%Y/',
        help_text="Program image"
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="Image caption or description"
    )
    priority = models.PositiveIntegerField(
        default=0,
        help_text="Display order"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['priority', '-uploaded_at']
        verbose_name = "Program Image"
        verbose_name_plural = "Program Images"
    
    def __str__(self):
        return f"{self.program.title} - Image {self.id}"


class ProgramUpdate(models.Model):
    """
    Progress updates and milestones for welfare programs.
    """
    
    program = models.ForeignKey(
        WelfareProgram,
        on_delete=models.CASCADE,
        related_name='updates',
        help_text="Related program"
    )
    title = models.CharField(
        max_length=200,
        help_text="Update title"
    )
    description = models.TextField(
        help_text="Update details"
    )
    image = models.ImageField(
        upload_to='programs/updates/%Y/',
        blank=True,
        null=True,
        help_text="Update image (optional)"
    )
    update_date = models.DateField(
        help_text="Date of this update"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-update_date']
        verbose_name = "Program Update"
        verbose_name_plural = "Program Updates"
    
    def __str__(self):
        return f"{self.program.title} - {self.title}"
