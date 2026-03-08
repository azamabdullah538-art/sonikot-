from django.contrib import admin
from django.utils.html import format_html
from .models import DonationCampaign, Donation, Donor

@admin.register(DonationCampaign)
class DonationCampaignAdmin(admin.ModelAdmin):
    """Admin for donation campaigns"""
    list_display = ['title', 'goal_amount', 'raised_amount', 'progress_bar', 'is_active', 'start_date', 'end_date']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['title', 'description']
    readonly_fields = ['raised_amount', 'created_at']
    date_hierarchy = 'start_date'

    fieldsets = (
        ('Campaign Information', {
            'fields': ('title', 'description', 'image')
        }),
        ('Funding Goals', {
            'fields': ('goal_amount', 'raised_amount')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
    )

    def progress_bar(self, obj):
        percentage = obj.progress_percentage
        color = 'success' if percentage >= 100 else 'primary' if percentage >= 50 else 'warning'
        return format_html(
            '<div class="progress" style="width: 100px;">'
            '<div class="progress-bar bg-{}" role="progressbar" style="width: {}%;" '
            'aria-valuenow="{}" aria-valuemin="0" aria-valuemax="100">{:.1f}%</div>'
            '</div>',
            color, percentage, percentage, percentage
        )
    progress_bar.short_description = 'Progress'

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    """Admin for donations"""
    list_display = ['donor_display', 'amount', 'donation_type', 'payment_method', 'campaign', 'created_at']
    list_filter = ['donation_type', 'payment_method', 'is_anonymous', 'created_at', 'campaign']
    search_fields = ['donor_name', 'donor_email', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    actions = ['mark_receipt_sent']

    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'donor_phone', 'donor_address', 'is_anonymous')
        }),
        ('Donation Details', {
            'fields': ('amount', 'donation_type', 'payment_method', 'transaction_id', 'campaign')
        }),
        ('Additional Information', {
            'fields': ('purpose', 'is_recurring', 'receipt_sent')
        }),
        ('Relations', {
            'fields': ('user',),
            'classes': ('collapse',)
        }),
    )

    def donor_display(self, obj):
        if obj.is_anonymous:
            return "Anonymous"
        return obj.donor_name
    donor_display.short_description = 'Donor'

    def mark_receipt_sent(self, request, queryset):
        updated = queryset.update(receipt_sent=True)
        self.message_user(request, f'{updated} receipt(s) marked as sent.')
    mark_receipt_sent.short_description = "Mark receipt as sent"

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    """Admin for recurring donors"""
    list_display = ['user', 'total_donated', 'donation_count', 'last_donation', 'is_recurring_donor']
    list_filter = ['is_recurring_donor', 'last_donation']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['total_donated', 'donation_count', 'last_donation']
