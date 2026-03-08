"""
URL Configuration for Programs App
"""

from django.urls import path
from . import views

app_name = 'programs'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/', views.program_detail, name='program_detail'),
]
