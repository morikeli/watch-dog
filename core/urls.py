from django.urls import path
from . import views


urlpatterns = [
    path('homepage/', views.HomepageView.as_view(), name='homepage'),
    path('map/', views.GeoMapView.as_view(), name='geo_map'),
    path('incidents/', views.IncidentsDetailView.as_view(), name='reported_incidents'),
    path('report-incident/', views.ReportIncidentsView.as_view(), name='report_incident'),
    
    path('wanted-suspects/', views.WantedSuspectsCreateView.as_view(), name='wanted_suspects'),
    path('suspect/<str:suspect_id>/update/', views.WantedSuspectsUpdateView.as_view(), name='update_suspect'),
]