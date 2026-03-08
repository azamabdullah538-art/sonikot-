"""
Leadership Models - Sonikot Youth Welfear Foundation

Professional database models for managing organization leadership.
"""

from django.db import models
from django.core.validators import RegexValidator
from django.utils.text import slugify
from django.urls import reverse


class ManagementPost(models.Model):
    """
    Defines available leadership positions in the organization.
    Examples: President, Vice President, Secretary, etc.
    """
    
    title = models.CharField(
        max_length=100,
        unique=True,
        help_text="Position title (e.g., President, General Secretary)"
    )
    priority = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower number = higher priority)"
    )
    description = models.TextField(
        blank=True,
        help_text="Brief description of the role"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Is this position currently active?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['priority', 'title']
        verbose_name = "Management Post"
        verbose_name_plural = "Management Posts"
    
    def __str__(self):
        return self.title


class OfficeBearer(models.Model):
    """
    Represents individuals holding leadership positions.
    Maintains current and historical leadership records.
    """
    
    STATUS_CHOICES = [
        ('current', 'Current'),
        ('former', 'Former'),
    ]
    
    # Phone number validator
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    # Personal Information
    full_name = models.CharField(
        max_length=200,
        help_text="Full name of the office bearer"
    )
    photo = models.ImageField(
        upload_to='images/',
        blank=True,
        null=True,
        help_text="Professional photo (recommended: 400x400px)"
    )
    
    # Position Details
    post = models.ForeignKey(
        ManagementPost,
        on_delete=models.PROTECT,
        related_name='office_bearers',
        help_text="Leadership position"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='current',
        help_text="Current or Former"
    )
    
    # Term Information
    term_start = models.DateField(
        help_text="Start date of the term"
    )
    term_end = models.DateField(
        blank=True,
        null=True,
        help_text="End date of the term (leave empty if current)"
    )
    
    # Contact Information
    email = models.EmailField(
        blank=True,
        help_text="Official email address"
    )
    phone = models.CharField(
        validators=[phone_validator],
        max_length=17,
        blank=True,
        help_text="Contact number"
    )
    
    # Additional Information
    bio = models.TextField(
        blank=True,
        help_text="Brief biography or achievements"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        help_text="Auto-generated URL slug"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-status', 'post__priority', '-term_start']
        verbose_name = "Office Bearer"
        verbose_name_plural = "Office Bearers"
        indexes = [
            models.Index(fields=['status', 'post']),
            models.Index(fields=['term_start', 'term_end']),
        ]
    
    def __str__(self):
        return f"{self.full_name} - {self.post.title}"
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided"""
        if not self.slug:
            base_slug = slugify(self.full_name)
            slug = base_slug
            counter = 1
            while OfficeBearer.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Get URL for individual office bearer detail page"""
        return reverse('leadership:bearer_detail', kwargs={'slug': self.slug})
    
    @property
    def is_current(self):
        """Check if this is a current office bearer"""
        return self.status == 'current'
    
    @property
    def term_duration(self):
        """Calculate term duration in years"""
        if self.term_end:
            delta = self.term_end - self.term_start
            return round(delta.days / 365, 1)
        return None


class LeadershipHistory(models.Model):
    """
    Records leadership transitions and important milestones.
    Useful for maintaining organizational history.
    """
    
    EVENT_TYPES = [
        ('appointment', 'Appointment'),
        ('resignation', 'Resignation'),
        ('election', 'Election'),
        ('transition', 'Transition'),
        ('milestone', 'Milestone'),
    ]
    
    office_bearer = models.ForeignKey(
        OfficeBearer,
        on_delete=models.CASCADE,
        related_name='history',
        help_text="Related office bearer"
    )
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        help_text="Type of event"
    )
    event_date = models.DateField(
        help_text="Date of the event"
    )
    description = models.TextField(
        help_text="Details about the event"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-event_date']
        verbose_name = "Leadership History"
        verbose_name_plural = "Leadership Histories"
    
    def __str__(self):
        return f"{self.office_bearer.full_name} - {self.event_type} ({self.event_date})"
