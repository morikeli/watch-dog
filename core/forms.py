from .models import Incident, Location, RoadAccident, FireIncident, ReportedCrime, WantedSuspect, ReportSuspect
from django import forms
from .utils import is_valid_media_file


class ReportIncidentForm(forms.ModelForm):
    INCIDENT_CHOICES = (
        (None, '-- Select type of incident --'),
        ('Crime', 'Crime'),
        ('Road accident', 'Road accident'),
    )
    REPORTER = (
        (None, '-- Who is reporting this incident --'),
        ('Witness', 'Witness'),
        ('Victim', 'Victim')
    )
    SEVERITY_LEVEL = (
        (None, '-- Select severity level --'),
        ('Low', 'Low'),
        ('Moderate', 'Moderate'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    )

    incident_type = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select',
        }),
        choices=INCIDENT_CHOICES,
        label='What type of incident are you reporting?',
    )
    incident_date = forms.DateField(widget=forms.DateInput(attrs={
            'type': 'date',
        }),
        help_text='Enter the date of the incident',
    )
    incident_time = forms.TimeField(widget=forms.TimeInput(attrs={
            'type': 'time',
        }),
        help_text='Enter the time of the incident',
        required=False,
    )
    description = forms.CharField(widget=forms.Textarea(attrs={
            'type': 'text',
            'placeholder': 'Provide more info. about the incident ...'
        }),
        help_text='How did the incident occur, who are the victims, was anyone injured?',
    )
    reported_by = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        label='Who is reporting the incident?',
        choices=REPORTER,
    )
    media_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'type': 'file', 'class': 'form-control', 'accept': '.3gpp, .jpg, .jpeg, .mp4, .mpeg, .ogg, .opus, .png, .wav',
        }),
        label='Media file (optional)',
        help_text='Upload video, image or audio file that can be used as an evidence.',
        required=False,
        validators=[is_valid_media_file],
    )

    class Meta:
        model = Incident
        fields = ('incident_type', 'incident_date', 'incident_time', 'description', 'reported_by', 'media_file')


class SubmitLocationForm(forms.ModelForm):
    county = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text',
        }),
        help_text='Enter the county where the incident occured'
    )
    sub_county = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text',
        }),
    )
    place = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text',
        }),
        label='Place of occurence',
        help_text='Enter the name of the place where the incident occured'
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
        fields = ('county', 'sub_county', 'place', 'landmark')


class ReportRoadAccidentForm(forms.ModelForm):
    ROAD_CONDITIONS = (
        (None, '-- Select road surface conditions --'),
        ('Dry', 'Dry'),
        ('Wet', 'Wet'),
        ('Slippery', 'Slippery')
    )

    ROAD_HAZARDS = (
        (None, '-- Select road surface hazards --'),
        ('Construction', 'Construction'),
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

    road = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text',
        }),
        help_text='Enter highway/road where the accident occurred',
        label='Road/Highway'
    )

    road_user = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
            'type': 'select',
        }),
        choices=ROAD_USER,
        help_text='Select road users involved in the accident',
        label='Type of road user',
    )

    vehicle_type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
            'type': 'select',
        }),
        choices=VEHICLE_TYPE,
        help_text='Select vehicle type involved in the road accident',
        label='Type of vehicle'
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
        ('Chemical', 'Chemical'),
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

    crime_type = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=CRIME_TYPE,
        label='Type of crime',
    )
    suspect_description = forms.CharField(widget=forms.Textarea())


    class Meta:
        model = ReportedCrime
        fields = ('crime_type', 'suspect_description')


class AddWantedSuspectsForm(forms.ModelForm):
    SELECT_CRIME = (
        (None, '-- Select crime committed --'),
        ('Child trafficking', 'Child trafficking'),
        ('Drug trafficking', 'Drug trafficking'),
        ('Fraud', 'Fraud'),
        ('Murder', 'Murder'),
        ('Robbery', 'Robbery'),
        ('Sexual assault', 'Sexual assault'),
    )
    SELECT_GENDER = (
        (None, "-- Select suspect's gender --"),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    SELECT_STATUS = (
        (None, '-- Select suspect status --'),
        ('Hiding', 'Hiding'),
        ('Apprehended', 'Apprehended'),
    )

    name = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 
        }),
        help_text='Enter the name of the suspect',
    )
    nickname = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 
        }),
        help_text='Enter the nickname of the suspect',
        required=False,
    )
    gender = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select',
        }),
        choices=SELECT_GENDER,
    )
    crime = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select',
        }),
        choices=SELECT_CRIME,
    )
    bounty = forms.CharField(widget=forms.NumberInput(attrs={
            'max': 100_000_000,
            'min': 0,
        }),
        help_text='Enter bounty in Kshs.',
    )
    last_seen_location = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 
        }),
        help_text='Enter last seen location of the suspect',
    )
    status = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select',
        }),
        choices=SELECT_STATUS,
    )
    suspect_description = forms.CharField(
        widget=forms.Textarea(),
        help_text='Provide suspect description: age, height, facial hair, skin complexion, any scars or wounds, etc.',
        required=False,
    )
    suspect_img = forms.FileField(
        widget=forms.FileInput(attrs={
            'type': 'file', 'class': 'form-control', 'accept': '.jpg, .jpeg, .png',
        }),
        required=False,
        validators=[is_valid_media_file],
    )

    class Meta:
        model = WantedSuspect
        fields = ('name', 'nickname', 'gender', 'crime', 'bounty', 'last_seen_location', 'status', 'suspect_description', 'suspect_img')


class EditWantedSuspectsDetailsForm(forms.ModelForm):
    SELECT_CRIME = (
        (None, '-- Select crime committed --'),
        ('Child trafficking', 'Child trafficking'),
        ('Drug trafficking', 'Drug trafficking'),
        ('Fraud', 'Fraud'),
        ('Murder', 'Murder'),
        ('Robbery', 'Robbery'),
        ('Sexual assault', 'Sexual assault'),
    )
    SELECT_GENDER = (
        (None, "-- Select suspect's gender --"),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    SELECT_STATUS = (
        (None, '-- Select suspect status --'),
        ('Hiding', 'Hiding'),
        ('Apprehended', 'Apprehended'),
    )

    name = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 
        }),
        help_text='Enter the name of the suspect',
    )
    nickname = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 
        }),
        help_text='Enter the nickname of the suspect',
        required=False,
    )
    gender = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select',
        }),
        choices=SELECT_GENDER,
    )
    crime = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select',
        }),
        choices=SELECT_CRIME,
    )
    bounty = forms.CharField(widget=forms.NumberInput(attrs={
            'max': 100_000_000,
            'min': 0,
        }),
        help_text='Enter bounty in Kshs.',
    )
    last_seen_location = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 
        }),
        help_text='Enter last seen location of the suspect',
    )
    status = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select',
        }),
        choices=SELECT_STATUS,
    )
    suspect_description = forms.CharField(
        widget=forms.Textarea(),
        help_text='Provide suspect description: age, height, facial hair, skin complexion, any scars or wounds, etc.',
        required=False,
    )
    suspect_img = forms.FileField(
        widget=forms.FileInput(attrs={
            'type': 'file', 'class': 'form-control', 'accept': '.jpg, .jpeg, .png',
        }),
        required=False,
        validators=[is_valid_media_file],
    )

    class Meta:
        model = WantedSuspect
        fields = ('name', 'nickname', 'gender', 'crime', 'bounty', 'last_seen_location', 'status', 'suspect_description', 'suspect_img')


class ReportWantedSuspectForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={
            'placeholder': 'Provide suspect description ...',
        }),
        help_text='Clothes, facial hair (beard, moustache), haircut, hairstyle, height or skin complexion.',
    )
    location = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text',
        }),
        help_text='Enter the sub county/city/estate and county you saw the suspect'
    )
    last_seen_date = forms.DateField(widget=forms.DateInput(attrs={
            'type': 'date'
        }),
        label='Last seen (date)',
        help_text='Provide the date you saw the suspect.',
        required=False,
    )
    last_seen_time = forms.TimeField(widget=forms.TimeInput(attrs={
            'type': 'time'
        }),
        label='Last seen (time)',
        help_text='Provide the time you saw the suspect.',
        required=False,
    )

    class Meta:
        model = ReportSuspect
        fields = ('description', 'location', 'last_seen_date', 'last_seen_time')