from django.urls import path
from . import views

app_name = 'leadership'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/', views.bearer_detail, name='bearer_detail'),
]
