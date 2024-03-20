from django.urls import path
from . import views


urlpatterns = [
    path('homepage/', views.HomepageView.as_view(), name='homepage'),
    path('map/', views.GeoMapView.as_view(), name='geo_map'),
    path('incidents/', views.IncidentsDetailView.as_view(), name='reported_incidents'),
    path('report-incident/', views.ReportIncidentsView.as_view(), name='report_incident'),
    
    path('<str:officer_id>/wanted-suspects/', views.WantedSuspectsCreateView.as_view(), name='wanted_suspects'),
]