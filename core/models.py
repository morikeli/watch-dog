from django.db import models


class Incident(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    incident_type = models.CharField(max_length=20, blank=False)
    incident_date = models.DateField(blank=False)
    incident_time = models.TimeField(null=True)
    description = models.TextField()
    additional_details = models.TextField()
    media_file = models.FileField(upload_to='incidents/media/files/', blank=True)
    severity_level = models.CharField(max_length=20, blank=False)
    date_reported = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-incident_date', '-incident_time']
    

    def __str__(self):
        return self.incident_type
    

class Location(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    incident_id = models.ForeignKey(Incident, on_delete=models.CASCADE, editable=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    county = models.CharField(max_length=30, blank=False)
    sub_county = models.CharField(max_length=30, blank=False)
    city = models.CharField(max_length=30, blank=False)
    landmark = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['date_created', 'county', 'sub_county', 'landmark']


    def __str__(self):
        return self.incident_id.incident_type


class RoadAccident(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, editable=False)
    road = models.CharField(max_length=30, blank=False)
    vehicles_count = models.PositiveIntegerField(default=0, blank=False, db_column='Total vehicles')
    injuries_count = models.PositiveIntegerField(default=0, blank=False, db_column='Injuries')
    fatalities_count = models.PositiveIntegerField(default=0, blank=False, db_column='Fatalities')
    road_conditions = models.CharField(max_length=20, blank=False)
    road_hazards = models.CharField(max_length=20, blank=False)
    traffic_conditions = models.CharField(max_length=20, blank=False)
    weather_conditions = models.CharField(max_length=20, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-date_created', 'road']
    
    
    def __str__(self):
        return self.road
    

class FireIncident(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, editable=False)
    fire_type = models.CharField(max_length=20, blank=False)
    property_damage = models.CharField(max_length=20, blank=False)
    cause = models.CharField(max_length=20, blank=False)
    response_time = models.TimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.fire_type
    

class ReportedCrime(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, editable=False)
    crime_type = models.CharField(max_length=30, blank=False)
    suspect_description = models.TextField()
    reported_by = models.CharField(max_length=30, blank=False)
    investigation_status = models.CharField(max_length=20, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-date_created', 'crime_type']
    

    def __str__(self):
        return self.crime_type
    
