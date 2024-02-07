from django.urls import path
from . import views


urlpatterns = [
    path('homepage/', views.HomepageView.as_view(), name='homepage'),
    
]