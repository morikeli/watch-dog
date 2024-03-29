from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib import auth
from .serializers import IncidentSerializer, UserSignupSerializer
from core.models import Incident


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']

        user = auth.authenticate(email=email, password=password)
        
        if user is None:
            raise AuthenticationFailed('INVALID CREDENTIALS!! Please try again later.')
        

        return Response({"message": "Welcome back"}, status=status.HTTP_200_OK)


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