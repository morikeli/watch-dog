from django.urls import path
from . import views
from . import validators


urlpatterns = [
    path('homepage/', views.HomepageView.as_view(), name='homepage'),
    path('map/', views.GeoMapView.as_view(), name='geo_map'),
    path('notifications', views.NotificationsDetailView.as_view(), name='notifications'),
    path('incidents/', views.IncidentsDetailView.as_view(), name='reported_incidents'),
    path('report-incident/', views.ReportIncidentsCreateView.as_view(), name='report_incident'),
    path('suspect/<str:suspect_id>/report/', views.ReportWantedSuspectsCreateView.as_view(), name='report_suspect'),
    path('incident/<str:incident_id>/details/', views.ReportedIncidentsAdditionalInfoCreateView.as_view(), name='provide_incident_info'),
    path('wanted-suspects/', views.WantedSuspectsCreateView.as_view(), name='wanted_suspects'),
    path('suspect/<str:suspect_id>/update/', views.WantedSuspectsUpdateView.as_view(), name='update_suspect'),
]

htmx_urlpatterns = [
    path('validate-date/', validators.validate_last_seen_date),
    path('validate-time/', validators.validate_last_seen_time),
]

urlpatterns += htmx_urlpatterns