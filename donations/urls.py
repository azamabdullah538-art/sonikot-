from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('', views.donation_home, name='home'),
    path('campaign/<int:pk>/', views.campaign_detail, name='campaign_detail'),
    path('donate/', views.donate, name='donate'),
    path('donate/<int:campaign_id>/', views.donate, name='donate_campaign'),
    path('success/', views.donation_success, name='success'),
    path('dashboard/', views.donor_dashboard, name='dashboard'),
]
