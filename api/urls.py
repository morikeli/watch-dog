from django.urls import path
from . import views


urlpatterns = [
    path('reported-incidents/', views.IncidentsAPIListView.as_view()),
    path('incident/accidents', views.RoadAccidentsDetailView.as_view()),
    path('incident/crimes', views.ReportedCrimesDetailView.as_view())
]