from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib import auth
from .serializers import (
    IncidentSerializer,
    UserSignupSerializer,
    RoadAccidentSpotSerializer,
    ReportedCrimesSerializer,
    WantedSuspectsSerializer,
)
from core.models import Incident, RoadAccident, ReportedCrime, WantedSuspect


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
            'data': {"username": username, "username": user.username},
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
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