from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class ProgramCategory(models.Model):
    """Category for organizing programs."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=20, default='primary', choices=[
        ('primary', 'Blue'),
        ('secondary', 'Gray'),
        ('success', 'Green'),
        ('danger', 'Red'),
        ('warning', 'Yellow'),
        ('info', 'Cyan'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Program Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Program(models.Model):
    """Program model for community initiatives."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    category = models.ForeignKey(
        ProgramCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='programs'
    )
    featured_image = models.ImageField(
        upload_to='programs/', 
        blank=True, 
        null=True
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    budget = models.CharField(max_length=100, blank=True)
    target_beneficiaries = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('programs:program_detail', args=[self.slug])
