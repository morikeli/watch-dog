from .models import Incident, Location, RoadAccident, FireIncident, ReportedCrime
from django.contrib import admin


@admin.register(Incident)
class IncidentsTable(admin.ModelAdmin):
    list_display = ['incident_type', 'incident_date', 'incident_time', 'severity_level', 'reported_by', 'date_reported']
    readonly_fields = ['incident_type', 'incident_date', 'incident_time', 'description', 'additional_details', 'media_file', 'severity_level']


@admin.register(Location)
class IncidentsLocationTable(admin.ModelAdmin):
    list_display = ['county', 'sub_county', 'city', 'longitude', 'latitude', 'landmark']
    readonly_fields = ['county', 'sub_county', 'city', 'longitude', 'latitude', 'landmark']


@admin.register(RoadAccident)
class RoadAccidentsTable(admin.ModelAdmin):
    list_display = ['road', 'vehicles_count', 'injuries_count', 'fatalities_count', 'road_conditions', 'road_hazards', 'traffic_conditions', 'weather_conditions']
    readonly_fields = ['road', 'vehicles_count', 'injuries_count', 'fatalities_count', 'road_conditions', 'road_hazards', 'traffic_conditions', 'weather_conditions']


@admin.register(FireIncident)
class FireIncidentsTable(admin.ModelAdmin):
    list_display = ['fire_type', 'property_damage', 'cause', 'response_time']
    readonly_fields = ['fire_type', 'property_damage', 'cause', 'response_time']


@admin.register(ReportedCrime)
class ReportedCrimesTable(admin.ModelAdmin):
    list_display = ['crime_type', 'reported_by', 'investigation_status']
    readonly_fields = ['crime_type', 'reported_by', 'investigation_status']

