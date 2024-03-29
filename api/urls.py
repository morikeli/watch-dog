from django.urls import path
from . import views


urlpatterns = [
    path('reported-incidents/', views.IncidentsAPIListView.as_view()),
]