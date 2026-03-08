from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DonationCampaign(models.Model):
    """Model for donation campaigns"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    raised_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='campaigns/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def progress_percentage(self):
        if self.goal_amount > 0:
            return min((self.raised_amount / self.goal_amount) * 100, 100)
        return 0

class Donation(models.Model):
    """Model for individual donations"""
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online Payment'),
        ('cheque', 'Cheque'),
    ]

    DONATION_TYPES = [
        ('general', 'General Donation'),
        ('campaign', 'Campaign Specific'),
        ('program', 'Program Specific'),
        ('emergency', 'Emergency Relief'),
    ]

    # Donor Information
    donor_name = models.CharField(max_length=100)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=20, blank=True)
    donor_address = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=False)

    # Donation Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPES, default='general')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, blank=True, help_text="Bank reference or online transaction ID")

    # Relations
    campaign = models.ForeignKey(DonationCampaign, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Additional Info
    purpose = models.TextField(blank=True, help_text="Specific purpose or message")
    is_recurring = models.BooleanField(default=False)
    receipt_sent = models.BooleanField(default=False)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.is_anonymous:
            return f"Anonymous Donation - ${self.amount}"
        return f"{self.donor_name} - ${self.amount}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update campaign raised amount if applicable
        if self.campaign:
            self.campaign.raised_amount = self.campaign.donation_set.aggregate(
                total=models.Sum('amount')
            )['total'] or 0
            self.campaign.save()

class Donor(models.Model):
    """Model for recurring donors"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_donated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    donation_count = models.PositiveIntegerField(default=0)
    last_donation = models.DateTimeField(null=True, blank=True)
    is_recurring_donor = models.BooleanField(default=False)
    preferred_payment_method = models.CharField(max_length=20, choices=Donation.PAYMENT_METHODS, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Total: ${self.total_donated}"
