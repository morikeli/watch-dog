from rest_framework import serializers
from core.models import Incident, Location, RoadAccident, ReportedCrime, WantedSuspect
from accounts.models import User


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
            instance.save()    
        return instance


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('longitude', 'latitude', 'county', 'sub_county', 'place', 'landmark')


class RoadAccidentSpotSerializer(serializers.ModelSerializer):
    location_id = LocationSerializer(instance='location_id', read_only=True)

    class Meta:
        model = RoadAccident
        fields = (
            'location_id', 'road', 'road_user', 'vehicle_type', 'vehicles_count', 'injuries_count', 'fatalities_count', 
            'road_conditions',  'road_hazards', 'traffic_conditions', 'weather_conditions'
        )


class ReportedCrimesSerializer(serializers.ModelSerializer):
    location_id = LocationSerializer(instance='location_id', read_only=True)

    class Meta:
        model = ReportedCrime
        fields = ('location_id', 'crime_type', 'suspect_description')


class WantedSuspectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WantedSuspect
        fields = '__all__'