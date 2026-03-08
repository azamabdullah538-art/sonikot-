from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class VolunteerOpportunity(models.Model):
    """Model for volunteer opportunities"""
    SKILL_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    COMMITMENT_TYPES = [
        ('one_time', 'One-time Event'),
        ('short_term', 'Short-term (1-3 months)'),
        ('long_term', 'Long-term (3+ months)'),
        ('flexible', 'Flexible'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(blank=True, help_text="Skills and requirements needed")
    responsibilities = models.TextField(blank=True, help_text="What the volunteer will do")
    benefits = models.TextField(blank=True, help_text="What the volunteer gains")

    skill_level = models.CharField(max_length=20, choices=SKILL_LEVELS, default='beginner')
    commitment_type = models.CharField(max_length=20, choices=COMMITMENT_TYPES, default='flexible')
    time_commitment = models.CharField(max_length=100, blank=True, help_text="e.g., 5 hours/week")

    location = models.CharField(max_length=200, blank=True)
    is_remote = models.BooleanField(default=False)
    contact_person = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)

    is_active = models.BooleanField(default=True)
    max_volunteers = models.PositiveIntegerField(default=0, help_text="0 means unlimited")
    current_volunteers = models.PositiveIntegerField(default=0)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    image = models.ImageField(upload_to='volunteer_opportunities/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def is_full(self):
        return self.max_volunteers > 0 and self.current_volunteers >= self.max_volunteers

    @property
    def spots_left(self):
        if self.max_volunteers == 0:
            return "Unlimited"
        return max(0, self.max_volunteers - self.current_volunteers)

class VolunteerApplication(models.Model):
    """Model for volunteer applications"""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    opportunity = models.ForeignKey(VolunteerOpportunity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Personal Information
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)

    # Application Details
    motivation = models.TextField(help_text="Why do you want to volunteer?")
    experience = models.TextField(blank=True, help_text="Relevant experience or skills")
    availability = models.TextField(help_text="When are you available?")
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)

    # References
    reference_name = models.CharField(max_length=100, blank=True)
    reference_phone = models.CharField(max_length=20, blank=True)
    reference_email = models.EmailField(blank=True)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    application_date = models.DateTimeField(auto_now_add=True)
    review_date = models.DateTimeField(null=True, blank=True)
    review_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.opportunity.title}"

    def save(self, *args, **kwargs):
        if self.status == 'approved' and not self.review_date:
            self.review_date = timezone.now()
            # Update opportunity volunteer count
            if self.opportunity.current_volunteers < self.opportunity.max_volunteers or self.opportunity.max_volunteers == 0:
                self.opportunity.current_volunteers += 1
                self.opportunity.save()
        super().save(*args, **kwargs)

class Volunteer(models.Model):
    """Model for active volunteers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    opportunities = models.ManyToManyField(VolunteerOpportunity, blank=True)
    total_hours = models.PositiveIntegerField(default=0)
    join_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # Contact info (can be different from user profile)
    phone = models.CharField(max_length=20, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)

    # Skills and interests
    skills = models.TextField(blank=True)
    interests = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Volunteer"
