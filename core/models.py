from phonenumber_field.modelfields import PhoneNumberField
from django.db import models


def police_station_img_directory(instance, filename):
    """ Images will be uploaded to MEDIA_ROOT/station_{post_name}/imgs/filename. """
    return f'station_{instance.post_name}/imgs/{filename}'


def wanted_suspect_img_directory(instance, filename):
    """ Images will be uploaded to MEDIA_ROOT/suspect_{suspect_name}/imgs/filename. """
    return f'suspect_{instance.name}/imgs/{filename}'


def reported_incidents_media_directory(instance, filename):
    """ Images will be uploaded to MEDIA_ROOT/incident_{id}/media/filename. """
    return f'incident_{str(instance.id)[16:23]}/media/{filename}'


class PoliceStation(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    post_name = models.CharField(max_length=60, blank=False)
    county = models.CharField(max_length=50, blank=False)
    sub_county = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=50, blank=False)
    mobile_1 = PhoneNumberField(blank=False, db_column='Mobile no. 1')
    mobile_2 = PhoneNumberField(db_column='Mobile no. 2')
    img = models.ImageField(upload_to=police_station_img_directory, default='station.png')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['post_name', 'county', 'sub_county']
    

    def __str__(self):
        return self.post_name


class Incident(models.Model):
    """
        This models map the structure of incidents table. Incidents can be classified into:
        - Crimes
        - Fire incidents
        - Road accidents
    """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    incident_type = models.CharField(max_length=20, blank=False)
    incident_date = models.DateField(null=True, blank=False)
    incident_time = models.TimeField(null=True, blank=False)
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
    """ Location of the reported incidents are stored here. """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    incident_id = models.ForeignKey(Incident, on_delete=models.CASCADE, editable=False, db_column='incident_id')
    latitude = models.FloatField()
    longitude = models.FloatField()
    county = models.CharField(max_length=30, blank=False)
    sub_county = models.CharField(max_length=30, blank=False)
    city = models.CharField(max_length=30, blank=False, db_column='incident_spot')
    landmark = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['date_created', 'county', 'sub_county', 'landmark']


    def __str__(self):
        return self.incident_id.incident_type


class RoadAccident(models.Model):
    """ This table stores details of the reported road accidents. """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, editable=False, db_column='location_id')
    road = models.CharField(max_length=30, blank=False)
    road_user = models.CharField(max_length=15, blank=False)
    vehicle_type = models.CharField(max_length=10, blank=False)
    vehicles_count = models.PositiveIntegerField(default=0, blank=False, db_column='total_vehicles')
    injuries_count = models.PositiveIntegerField(default=0, blank=False, db_column='total_injuries')
    fatalities_count = models.PositiveIntegerField(default=0, blank=False, db_column='total_fatalities')
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
    """ This table stores details about reported fire incidents. """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, editable=False, db_column='location_id')
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
    """ This table stores details about reported crimes. """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, editable=False, db_column='location_id')
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
    

class WantedSuspect(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=50, blank=False)
    nickname = models.CharField(max_length=30, blank=False)
    gender = models.CharField(max_length=7, blank=False)
    bounty = models.PositiveIntegerField(default=0)
    crime = models.CharField(max_length=30, blank=False)
    status = models.CharField(max_length=30, blank=False)
    suspect_img = models.ImageField(upload_to=wanted_suspect_img_directory, default='default.png')
    last_seen_location = models.CharField(max_length=30, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['name', 'gender']

    
    def __str__(self):
        return self.name