"""
Core Models - Sonikot Youth Welfear Foundation

Professional database models for core functionality:
- Contact form submissions
- Gallery images
- Testimonials
- Site settings
"""

from django.db import models
from django.core.validators import EmailValidator


class ContactSubmission(models.Model):
    """
    Stores contact form submissions from website visitors.
    """
    
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('donation', 'Donation Related'),
        ('volunteer', 'Volunteer Inquiry'),
        ('partnership', 'Partnership Proposal'),
        ('complaint', 'Complaint/Feedback'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('resolved', 'Resolved'),
    ]
    
    # Contact Information
    full_name = models.CharField(
        max_length=200,
        help_text="Sender's full name"
    )
    email = models.EmailField(
        validators=[EmailValidator()],
        help_text="Sender's email address"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Sender's phone number (optional)"
    )
    
    # Message Details
    subject = models.CharField(
        max_length=30,
        choices=SUBJECT_CHOICES,
        default='general',
        help_text="Message subject category"
    )
    message = models.TextField(
        help_text="Message content"
    )
    
    # Management
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        help_text="Submission status"
    )
    admin_notes = models.TextField(
        blank=True,
        help_text="Internal notes (not visible to sender)"
    )
    
    # Metadata
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        help_text="Sender's IP address"
    )
    user_agent = models.CharField(
        max_length=300,
        blank=True,
        help_text="Browser user agent"
    )
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"
        indexes = [
            models.Index(fields=['status', '-submitted_at']),
        ]
    
    def __str__(self):
        return f"{self.full_name} - {self.subject} ({self.submitted_at.strftime('%Y-%m-%d')})"
    
    @property
    def is_new(self):
        """Check if submission is new"""
        return self.status == 'new'


class GalleryCategory(models.Model):
    """
    Categories for organizing gallery images.
    Examples: Events, Programs, Community, Achievements
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Category name"
    )
    description = models.TextField(
        blank=True,
        help_text="Category description"
    )
    priority = models.PositiveIntegerField(
        default=0,
        help_text="Display order"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Is this category active?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['priority', 'name']
        verbose_name = "Gallery Category"
        verbose_name_plural = "Gallery Categories"
    
    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    """
    Individual images in the gallery.
    """
    
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.PROTECT,
        related_name='images',
        help_text="Image category"
    )
    title = models.CharField(
        max_length=200,
        help_text="Image title"
    )
    image = models.ImageField(
        upload_to='gallery/%Y/%m/',
        help_text="Gallery image (recommended: 1200x800px)"
    )
    description = models.TextField(
        blank=True,
        help_text="Image description or story"
    )
    event_date = models.DateField(
        blank=True,
        null=True,
        help_text="Date when photo was taken"
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        help_text="Photo location"
    )
    photographer = models.CharField(
        max_length=100,
        blank=True,
        help_text="Photographer name"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Feature on homepage?"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Show on website?"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_featured', '-uploaded_at']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
    
    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """
    Testimonials from beneficiaries, volunteers, or supporters.
    """
    
    full_name = models.CharField(
        max_length=200,
        help_text="Person's name"
    )
    role = models.CharField(
        max_length=100,
        blank=True,
        help_text="Role or designation (e.g., Beneficiary, Volunteer)"
    )
    photo = models.ImageField(
        upload_to='testimonials/',
        blank=True,
        null=True,
        help_text="Person's photo (optional)"
    )
    testimonial = models.TextField(
        help_text="Testimonial text"
    )
    rating = models.PositiveSmallIntegerField(
        default=5,
        choices=[(i, str(i)) for i in range(1, 6)],
        help_text="Rating out of 5"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Show on homepage?"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Show on website?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
    
    def __str__(self):
        return f"{self.full_name} - {self.rating}/5"


class SiteSettings(models.Model):
    """
    Global site settings (should only have one instance).
    """
    
    # About Organization
    mission = models.TextField(
        blank=True,
        help_text="Organization mission statement"
    )
    vision = models.TextField(
        blank=True,
        help_text="Organization vision statement"
    )
    values = models.TextField(
        blank=True,
        help_text="Core values (one per line)"
    )
    history = models.TextField(
        blank=True,
        help_text="Organization history"
    )
    about_text = models.TextField(
        blank=True,
        help_text="About page main text"
    )
    
    # Homepage Settings
    hero_title = models.CharField(
        max_length=200,
        default="Serving Humanity with Compassion",
        help_text="Homepage hero section title"
    )
    hero_subtitle = models.CharField(
        max_length=300,
        blank=True,
        help_text="Homepage hero section subtitle"
    )
    hero_image = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True,
        help_text="Homepage hero background image"
    )
    
    # Statistics (for homepage)
    total_beneficiaries = models.PositiveIntegerField(
        default=0,
        help_text="Total people helped"
    )
    active_programs = models.PositiveIntegerField(
        default=0,
        help_text="Number of active programs"
    )
    volunteers_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of volunteers"
    )
    years_of_service = models.PositiveIntegerField(
        default=1,
        help_text="Years in operation"
    )
    
    # Social Media Links
    facebook_url = models.URLField(blank=True, help_text="Facebook page URL")
    twitter_url = models.URLField(blank=True, help_text="Twitter profile URL")
    instagram_url = models.URLField(blank=True, help_text="Instagram profile URL")
    youtube_url = models.URLField(blank=True, help_text="YouTube channel URL")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn page URL")
    whatsapp_number = models.CharField(max_length=20, blank=True, help_text="WhatsApp number with country code")
    
    # Footer
    footer_text = models.TextField(
        blank=True,
        help_text="Footer description text"
    )
    
    # Meta
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return "Site Settings"
    
    def save(self, *args, **kwargs):
        """Ensure only one instance exists"""
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        """Load site settings (creates if doesn't exist)"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
