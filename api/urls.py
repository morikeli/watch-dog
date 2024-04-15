from django.urls import path
from . import views


urlpatterns = [
    path('auth/login', views.LoginView.as_view()),
    path('auth/signup', views.SignupView.as_view()),
    path('reported-incidents/', views.IncidentsAPIListView.as_view()),
    path('incidents/location', views.IncidentLocationsListView.as_view()),
    path('incident/accidents', views.RoadAccidentsDetailView.as_view()),
    path('incident/crimes', views.ReportedCrimesDetailView.as_view()),
    path('wanted-suspects', views.WantedSuspectsDetailView.as_view()),
]