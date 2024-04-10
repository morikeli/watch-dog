from django.db.models.signals import post_save, pre_save
from django.core.management.base import BaseCommand
from django.dispatch import receiver
from django.conf import settings
from core.models import Incident, IncidentLocation, RoadAccident
import pandas as pd
import requests
import environ
import os
import random


env = environ.Env()
environ.Env.read_env()


class Command(BaseCommand):
    help = 'Load data from an Excel spreadsheet (.xlsx) or .csv files.'

    API_KEY = env('API_KEY')
    API_DOMAIN = env('API_DOMAIN')
    folder_path = settings.BASE_DIR/'data/csv/road-accidents/'
    

    def handle(self, *args, **kwargs):
        files = os.listdir(self.folder_path)
        for file_name in files:
            file_path = os.path.join(self.folder_path, file_name)

            if file_name.endswith('.csv'):
                self.import_csv(file_path)
            
            elif file_name.endswith('.xlsx'):
                self.import_excel(file_path)
            
            else:
                self.stdout.write(self.style.ERROR('Unsupported file format!'))


    def import_csv(self, file_path):
        df = pd.read_csv(file_path)
        self.process_data(df)


    def import_excel(self, file_path):
        df = pd.read_excel(file_path)
        self.process_data(df)
    

    def process_data(self, df):
        for index, row in df.iterrows():
            incident, _ = Incident.objects.get_or_create(
                incident_type='Road accident',
                description=row['BRIEF ACCIDENT DETAILS'],
                severity_level=random.randint(1, 5)
            )
            
            address = f"{str(row['BASE/SUB BASE']).capitalize()}, {str(row['COUNTY']).capitalize()} - Kenya"

            # fetch coordinates of the location where an accident occured.
            BASE_URL = f"{self.API_DOMAIN}?q={address}&key={self.API_KEY}&format=json"
            response = requests.get(BASE_URL)

            # Check the response HTTP status code
            if response.status_code == 200:
                # Parse the JSON data from the response
                data = response.json()

                # get longitude and latitude of the generated data.
                latitude = data[0]["lat"]
                longitude = data[0]["lon"]

            elif response.status_code == 404:   # if HTTP_404 is generated 
                latitude = latitude
                longitude = longitude
            
            self.stdout.write(self.style.HTTP_INFO(f'Row {index} | Latitude: {latitude} | Longitude: {longitude}'))

            location, _ = Location.objects.get_or_create(
                incident_id=incident,
                longitude=longitude,
                latitude=latitude,
                county=row['COUNTY'],
                sub_county=row['BASE/SUB BASE'],
                city=row['PLACE'],
            )

            accident, _ = RoadAccident.objects.get_or_create(
                location_id=location,
                road=row['ROAD'],
                road_user=row['VICTIM'],
                vehicle_type=row['MV INVOLVED'],
                injuries_count=0 if str(row['NO.']) == 'NaN' or  str(row['NO.']) == 'nan' else row['NO.']
            )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
