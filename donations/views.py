from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum
from .models import DonationCampaign, Donation, Donor
from .forms import DonationForm

def donation_home(request):
    """Main donations page with active campaigns"""
    campaigns = DonationCampaign.objects.filter(is_active=True).order_by('-created_at')
    total_raised = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_donors = Donation.objects.values('donor_email').distinct().count()

    context = {
        'campaigns': campaigns,
        'total_raised': total_raised,
        'total_donors': total_donors,
    }
    return render(request, 'donations/home.html', context)

def campaign_detail(request, pk):
    """Detailed view of a donation campaign"""
    campaign = get_object_or_404(DonationCampaign, pk=pk, is_active=True)
    donations = Donation.objects.filter(campaign=campaign, is_anonymous=False).order_by('-created_at')[:10]

    context = {
        'campaign': campaign,
        'donations': donations,
        'progress_percentage': campaign.progress_percentage,
    }
    return render(request, 'donations/campaign_detail.html', context)

def donate(request, campaign_id=None):
    """Handle donation form submission"""
    campaign = None
    if campaign_id:
        campaign = get_object_or_404(DonationCampaign, pk=campaign_id, is_active=True)

    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            if campaign:
                donation.campaign = campaign
            if request.user.is_authenticated:
                donation.user = request.user
            donation.save()

            # Send confirmation email
            try:
                send_mail(
                    'Donation Receipt - Sonikot Youth Welfear Foundation',
                    f'Thank you for your generous donation of ${donation.amount}.\n\n'
                    f'Donation ID: {donation.id}\n'
                    f'Date: {donation.created_at.strftime("%Y-%m-%d")}\n\n'
                    f'Sonikot Youth Welfear Foundation',
                    settings.DEFAULT_FROM_EMAIL,
                    [donation.donor_email],
                    fail_silently=True,
                )
            except:
                pass

            messages.success(request, 'Thank you for your donation! A receipt has been sent to your email.')
            return redirect('donations:success')
    else:
        form = DonationForm()

    context = {
        'form': form,
        'campaign': campaign,
    }
    return render(request, 'donations/donate.html', context)

def donation_success(request):
    """Success page after donation"""
    return render(request, 'donations/success.html')

def donor_dashboard(request):
    """Dashboard for logged-in donors"""
    if not request.user.is_authenticated:
        return redirect('login')

    donations = Donation.objects.filter(user=request.user).order_by('-created_at')
    total_donated = donations.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'donations': donations,
        'total_donated': total_donated,
    }
    return render(request, 'donations/dashboard.html', context)
