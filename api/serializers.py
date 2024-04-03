from rest_framework import serializers
from core.models import Incident, Location, RoadAccident, ReportedCrime
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


class RoadAccidentSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadAccident
        fields = (
            'location_id', 'road', 'road_user', 'vehicle_type', 'vehicles_count', 'injuries_count', 'fatalities_count', 
            'road_conditions',  'road_hazards', 'traffic_conditions', 'weather_conditions'
        )


class ReportedCrimesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedCrime
        fields = ('crime_type', 'suspect_description')