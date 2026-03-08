from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    """Form for making donations"""
    class Meta:
        model = Donation
        fields = [
            'donor_name', 'donor_email', 'donor_phone', 'donor_address',
            'amount', 'donation_type', 'payment_method', 'transaction_id',
            'purpose', 'is_anonymous'
        ]
        widgets = {
            'donor_address': forms.Textarea(attrs={'rows': 3}),
            'purpose': forms.Textarea(attrs={'rows': 3}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make certain fields not required for anonymous donations
        for field in ['donor_name', 'donor_email', 'donor_phone', 'donor_address']:
            self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()
        is_anonymous = cleaned_data.get('is_anonymous')
        amount = cleaned_data.get('amount')

        if not is_anonymous:
            # Require name and email for non-anonymous donations
            if not cleaned_data.get('donor_name'):
                raise forms.ValidationError("Donor name is required for non-anonymous donations.")
            if not cleaned_data.get('donor_email'):
                raise forms.ValidationError("Donor email is required for non-anonymous donations.")

        if amount and amount <= 0:
            raise forms.ValidationError("Donation amount must be greater than zero.")

        return cleaned_data
