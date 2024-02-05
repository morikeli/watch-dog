from .models import Incident, Location, RoadAccident, FireIncident, ReportedCrime
from django import forms
from .utils import is_valid_media_file


class ReportIncidentForm(forms.ModelForm):
    INCIDENT_CHOICES = (
        (None, '-- Select type of incident'),
        ('Crime', 'Crime'),
        ('Fire incident', 'Fire incident'),
        ('Road accident', 'Road accident'),
    )

    SEVERITY_LEVEL = (
        (None, '-- Select severity level --'),
        ('Low', 'Low'),
        ('Moderate', 'Moderate'),
        ('High', 'High'),
        ('Critical', 'Critical'),
        ('Non-critical', 'Non-critical'),
    )

    incident_type = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=INCIDENT_CHOICES
    )
    incident_date = forms.DateField(widget=forms.DateInput(attrs={
            'type': 'date', 'class': 'mb-1'
        }),
        help_text='Enter the date of the incident',
    )
    incident_time = forms.TimeField(widget=forms.TimeInput(attrs={
            'type': 'time', 'class': 'mb-1'
        }),
        help_text='Enter the time of the incident',
        required=False,
    )
    description = forms.CharField(widget=forms.Textarea())
    additional_details = forms.CharField(widget=forms.Textarea())
    media_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'type': 'file', 'class': 'form-control mb-2', 'accept': '.3gpp, .jpg, .jpeg, .mp4, .mpeg, .ogg, .opus, .png, .wav',
        }),
        required=False,
        validators=[is_valid_media_file],
    )

    class Meta:
        model = Incident
        fields = ('incident_type', 'incident_date', 'incident_time', 'description', 'additional_details', 'media_file')


class SubmitLocationForm(forms.ModelForm):
    county = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 'class': 'mb-2',
        }),
        help_text='Enter the county where the incident occured'
    )
    sub_county = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 'class': 'mb-2',
        }),
    )
    city = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 'class': 'mb-2',
        }),
        label='City/Estate/Village',
        help_text='Enter the city/estate/village where the incident occured'
    )
    landmark = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text',
        }),
        help_text='Enter the name of the building, industry, bus stage, market, river or road',
        label='Nearest landmark',
        required=False,
    )

    class Meta:
        model = Location
        fields = ('county', 'sub_county', 'city', 'landmark')


class ReportRoadAccidentForm(forms.ModelForm):
    ROAD_CONDITIONS = (
        (None, '-- Select road surface conditions --'),
        ('Dry', 'Dry'),
        ('Wet', 'Wet'),
        ('Slippery', 'Slippery')
    )

    ROAD_HAZARDS = (
        (None, '-- Select road surface hazards --'),
        ('Construction', 'Construction')
        ('Debris', 'Debris'),
        ('Potholes', 'Potholes')
    )
    
    ROAD_USER = (
        (None, '-- Select road user'),
        ('Cyclist', 'Cyclist'),
        ('Driver', 'Driver'),
        ('Motorcyclist', 'Motorcyclist'),
        ('Passenger', 'Passenger'),
        ('Pedestrian', 'Pedestrian'),
    )

    VEHICLE_TYPE = (
        (None, '-- Select type of vehicle --'),
        ('Bicycle', 'Bicycle'),
        ('Bus', 'Bus'),
        ('Lorry', 'Lorry/Truck'),
        ('Motorcycle', 'Motorcycle'),
        ('Motor vehicle', 'Motor vehicle'),
        ('Truck', 'Trailer'),
        ('Tuktuk', 'Tuktuk'),
        ('Van', 'Van')
    )

    TRAFFIC_CONDITIONS = (
        (None, '-- Select road surface conditions --'),
        ('Congestion', 'Congestion'),
        ('Gridlock', 'Gridlock'),
        ('Heavy traffic', 'Heavy traffic')
    )
    
    WEATHER_CONDITIONS = (
        (None, '-- Select road surface conditions --'),
        ('Clear sky', 'Clear sky'),
        ('Drizzle', 'Drizzle'),
        ('Foggy', 'Foggy'),
        ('Heavy rains', 'Heavy rains'),
        ('Windy', 'Windy')
    )

    road = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select',
        }),
        help_text='Enter highway/road where the accident occurred',
        label='Road/Highway'
    )

    road_user = forms.ChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
            'type': 'select',
        }, choices=ROAD_USER),
        help_text='Enter highway/road where the accident occurred',
        label='Road/Highway',
    )

    vehicle_type = forms.ChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
            'type': 'select',
        }, choices=VEHICLE_TYPE),
        help_text='Enter highway/road where the accident occurred',
        label='Road/Highway'
    )
    
    vehicles_count = forms.CharField(widget=forms.NumberInput(attrs={
            'type': 'number', 'min': 0,
        }),
        help_text='Enter the number of vehicles involved in the accident',
        label='Total vehicles involved'
    )
    injuries_count = forms.CharField(widget=forms.NumberInput(attrs={
            'type': 'number', 'min': 0,
        }),
        help_text='Enter the number of victims injured in the accident',
        label='Injured vitims'
    )
    fatalities_count = forms.CharField(widget=forms.NumberInput(attrs={
            'type': 'number', 'min': 0,
        }),
        help_text='Enter the fatalities count of the accident',
        label='Fatalities'
    )
    road_conditions = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=ROAD_CONDITIONS
    )
    road_hazards = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=ROAD_HAZARDS
    )
    traffic_conditions = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=TRAFFIC_CONDITIONS
    )
    weather_conditions = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=WEATHER_CONDITIONS
    )

    class Meta:
        model = RoadAccident
        fields = (
            'road', 'road_user', 'vehicle_type', 'vehicles_count', 'injuries_count', 'fatalities_count', 
            'road_conditions',  'road_hazards', 'traffic_conditions', 'weather_conditions'
        )


class ReportFireIncidentForm(forms.ModelForm):
    FIRE_TYPE = (
        (None, '-- Select fire category --'),
        ('Building fire', 'Building fire'),
        ('Forest fire', 'Forest fire'),
        ('Industrial fire', 'Industrial fire'),
        ('Wildfire', 'Wildfire'),
    )

    PROPERTY_DAMAGE = (
        (None, '-- Select degree of property damage --'),
        ('Minimal', 'Minimal'),
        ('Moderate', 'Moderate'),
        ('Severe', 'Severe'),
        ('Total loss', 'Total loss'),
        ('No damage', 'No damage'),
    )

    CAUSE_OF_FIRE = (
        (None, '-- Select the cause of fire --'),
        ('Accidental', 'Accidental'),
        ('Appliance malfunction', 'Appliance malfunction'),
        ('Arson', 'Arson'),
        ('Chemical', 'Chemical')
        ('Electrical', 'Electrical'),
        ('Heating equipment', 'Heating equipment'),
        ('Human error', 'Human error'),
        ('Outdoor burning', 'Outdoor burning'),
        ('Smoking', 'Smoking'),
        ('Spontaneous combustion', 'Spontaneous combustion'),
        ('Vehicle', 'Vehicle')
    )
    
    fire_type = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=FIRE_TYPE
    )
    property_damage = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=PROPERTY_DAMAGE
    )
    cause = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        label='Cause of fire',
        choices=CAUSE_OF_FIRE
    )

    class Meta:
        model = FireIncident
        fields = ('fire_type', 'property_damage', 'cause', 'response_time')


class ReportCrimesForm(forms.ModelForm):
    CRIME_TYPE = (
        (None, '-- Select type of crime --'),
        ('Assault', 'Assault'),
        ('Theft', 'Theft'),
        ('Vandalism', 'Vandalism'),
    )
    REPORTER = (
        (None, '-- Who is reporting this crime --'),
        ('Witness', 'Witness'),
        ('Law enforcement', 'Law enforcement'),
        ('Victim', 'Victim')
    )


    crime_type = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=CRIME_TYPE,
        label='Type of crime',
    )
    suspect_description = forms.CharField(widget=forms.Textarea())
    reported_by = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        label='User',
        choices=REPORTER,
    )

    class Meta:
        model = ReportedCrime
        fields = ('crime_type', 'suspect_description', 'reported_by')