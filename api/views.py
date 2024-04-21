from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib import auth
from .serializers import (
    IncidentSerializer,
    LocationSerializer,
    SignupSerializer,
    RoadAccidentSpotSerializer,
    ReportedCrimesSerializer,
    WantedSuspectsSerializer,
)
from core.models import Incident, IncidentLocation, RoadAccident, ReportedCrime, WantedSuspect
import requests
import environ


env = environ.Env()
environ.Env.read_env()


class LoginView(APIView):
    authentication_classes = [BasicAuthentication]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = auth.authenticate(username=username, password=password)
        
        if user is None:
            raise AuthenticationFailed('INVALID CREDENTIALS!! Please try again later.')
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'data': {"username": username},
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IncidentsAPIListView(APIView):
    pagination_class = PageNumberPagination
    

    def get(self, request, *args, **kwargs):
        incidents = Incident.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(incidents, request)
        serializer = IncidentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    authentication_classes = [BasicAuthentication]
    def post(self, request, *args, **kwargs):
        serializer = IncidentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IncidentLocationsListView(APIView):
    API_KEY = env('API_KEY')
    API_DOMAIN = env('API_DOMAIN')


    def get(self, request, *args, **kwargs):
        locations_qs = IncidentLocation.objects.all()
        serializer = LocationSerializer(locations_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request, *args, **kwargs):
        latest_incident = Incident.objects.first()
        
        try:
            # geocode location
            address = f"{str(request.data['place']).capitalize()}, {str(request.data['sub_county']).capitalize()}, {str(request.data['county']).capitalize()}, Kenya"
            BASE_URL = f"{self.API_DOMAIN}?q={address}&key={self.API_KEY}&format=json"
            response = requests.get(BASE_URL)

            # Check the response HTTP status code
            if response.status_code == 200:
                # Parse the JSON data from the response
                data = response.json()

                # get longitude and latitude of the generated data.
                latitude = data[0]["lat"]
                longitude = data[0]["lon"]
            
            location_data = {
                'county': request.data['county'],
                'sub_county': request.data['sub_county'],
                'longitude': longitude,
                'latitude': latitude,
                'place': request.data['place'],
                'landmark': request.data['landmark'],
            }

            serializer = LocationSerializer(data=location_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(incident_id=latest_incident)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
                

        except (requests.ConnectionError, requests.ConnectTimeout):
            return Response({"message": "Please check your internet connection!"}, status=status.HTTP_408_REQUEST_TIMEOUT)
        


class RoadAccidentsDetailView(APIView):
    pagination_class = PageNumberPagination


    def get(self, request, *args, **kwargs):
        accidents_qs = RoadAccident.objects.all()
        paginator = self.pagination_class()
        results_page = paginator.paginate_queryset(accidents_qs, request)
        serializer = RoadAccidentSpotSerializer(results_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ReportedCrimesDetailView(APIView):
    pagination_class = PageNumberPagination


    def get(self, request, *args, **kwargs):
        crimes_qs = ReportedCrime.objects.all()
        serializer = ReportedCrimesSerializer(crimes_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WantedSuspectsDetailView(APIView):
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        suspects_qs = WantedSuspect.objects.all()
        paginator = self.pagination_class()
        results_page = paginator.paginate_queryset(suspects_qs, request)
        serializer = WantedSuspectsSerializer(results_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class LogoutUserView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {"message": "User logged out ..."}

        return response