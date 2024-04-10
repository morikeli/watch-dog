from .forms import (
    AddWantedSuspectsForm, 
    EditWantedSuspectsDetailsForm,
    ReportIncidentForm, 
    ReportRoadAccidentForm, 
    ReportCrimesForm, 
    ReportWantedSuspectForm,
    SubmitLocationForm, 
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.files.storage import FileSystemStorage
from django.utils.decorators import method_decorator
from django.utils import timezone
from formtools.wizard.views import SessionWizardView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from django.views import View
from .models import Incident, IncidentLocation, RoadAccident, ReportedCrime, WantedSuspect, Notification
import environ
import requests
import os


@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False), name='get')
class HomepageView(View):
    template_name = 'core/homepage.html'

    def get(self, request, *args, **kwargs):
        total_accidents = Incident.objects.filter(incident_type='Road accident').count()
        total_crimes = Incident.objects.filter(incident_type='Crime').count()
        incidents_qs = Incident.objects.all()[:15]
        suspect_qs = WantedSuspect.objects.all()

        # update user's feed based on his/her current location.
        current_dt = timezone.now()
        start_dt = current_dt - timezone.timedelta(hours=24)    # set filter datetime to the last 24hrs from the current datetime
        location_qs = IncidentLocation.objects.filter(date_created__gte=start_dt).order_by('-incident_id__date_reported')

        # pagination
        p = Paginator(location_qs, 8)
        page_number = request.GET.get('page')

        try:
            page_obj = p.get_page(page_number)

        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = p.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = p.page(p.num_pages)


        context = {
            'TotalRoadAccidents': total_accidents,
            'TotalReportedCrimes': total_crimes,
            'reported_incidents': incidents_qs,
            'wanted_suspects': suspect_qs,
            'incidents_feed': page_obj,
            'page_obj': page_obj,
            'page': page_obj,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False), name='get')
class NotificationsDetailView(View):
    template_name = 'core/notifications.html'

    def get(self, request, *args, **kwargs):
        notifications_qs = Notification.objects.all()
        context = {'notifications': notifications_qs}
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False), name='get')
class ReportWantedSuspectsCreateView(View):
    form_class = ReportWantedSuspectForm
    template_name = 'core/report-suspect.html'

    def get(self, request, suspect_id, *args, **kwargs):
        suspect_obj = WantedSuspect.objects.get(id=suspect_id)
        form = self.form_class()

        context = {'ReportSuspectForm': form, 'suspect': suspect_obj}
        return render(request, self.template_name, context)
    

    def post(self, request, suspect_id, *args, **kwargs):
        suspect_obj = WantedSuspect.objects.get(id=suspect_id)
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            create_suspect = form.save(commit=False)
            create_suspect.suspect = suspect_obj
            create_suspect.save()

            messages.success(request, 'Suspect details successfully submitted!')
            return redirect('homepage')

        context = {'ReportSuspectForm': form}
        return render(request, self.template_name, context)


class ReportIncidentsCreateView(SessionWizardView):
    env = environ.Env()
    environ.Env.read_env()
    API_KEY = env('API_KEY')
    API_DOMAIN = env('API_DOMAIN')
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))
    form_list = [ReportIncidentForm, SubmitLocationForm]
    template_name = 'core/report-incident.html'


    def done(self, form_list, **kwargs):
        form = form_list[0]

        if form.is_valid():
            reported_incident = form.save()
            location_form = form_list[1].save(commit=False)
            location_form.incident_id = reported_incident

            # get county and sub county provided in the form
            county = form_list[1].cleaned_data['county']
            sub_county = form_list[1].cleaned_data['sub_county']
            place = location_form.place

            # geocode location
            address = f"{str(place).capitalize()}, {str(sub_county).capitalize()}, {str(county).capitalize()}, Kenya"
            BASE_URL = f"{self.API_DOMAIN}?q={address}&key={self.API_KEY}&format=json"
            response = requests.get(BASE_URL)

            # Check the response HTTP status code
            if response.status_code == 200:
                # Parse the JSON data from the response
                data = response.json()

                # get longitude and latitude of the generated data.
                latitude = data[0]["lat"]
                longitude = data[0]["lon"]
            
            location_form.longitude = longitude
            location_form.latitude = latitude
            location_form.save()

            messages.success(self.request, 'Incident reported successfully!')
            return redirect('report_incident')
        
        messages.error(self.request, 'ERROR!! The form could not be submitted!')
        return redirect('report_incident')


@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False), name='get')
class GeoMapView(View):
    template_name = 'core/map.html'

    def get(self, request, *args, **kwargs):
        current_dt = timezone.now()
        start_dt = current_dt - timezone.timedelta(hours=24)    # set filter datetime to the last 24hrs from the current datetime
        # get coordinates for reportted crimes and accidents
        incidents_qs = IncidentLocation.objects.filter(date_created__gte=start_dt).values(
            'longitude', 
            'latitude', 
            'county', 
            'sub_county', 
            'place',
            'incident_id__incident_type',
            'incident_id__incident_date',
            'incident_id__incident_time',
            'incident_id__reported_by',
        )
        
        # Rename keys in the dictionaries from querysets - accidents_qs and crimes_qs
        # dictionariies generated using .values() have a key - 'location_id_longitude' or 'location_id_latitude'
        # updated these keys to 'longitude' and 'latitude' using list comprehension
        incident_spots = [
            {
                "latitude": round(location["latitude"], 4), 
                "longitude": round(location["longitude"], 4),
                "county": location["county"],
                "sub_county": location["county"],
                "place": location["place"],
                "incident_type": location["incident_id__incident_type"],
                "incident_date": location["incident_id__incident_date"],
                "incident_time": location["incident_id__incident_time"],
                "reported_by": location["incident_id__reported_by"],
            } for location in incidents_qs
        ]

        context = {'incident_locations': incident_spots}
        return render(request, self.template_name, context)
    

@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False), name='get')
class IncidentsDetailView(View):
    template_name = 'core/incidents.html'

    def get(self, request, *args, **kwargs):
        incidents_qs = Incident.objects.all()
        
        context = {'reported_incidents': incidents_qs}
        return render(request, self.template_name, context)


# officers views
@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: user.is_officer is True and user.is_roadsafetystaff is False and user.is_staff is False and user.is_superuser is False), name='get')
class ReportedIncidentsAdditionalInfoCreateView(View):
    form_class = {'AccidentsForm': ReportRoadAccidentForm, 'CrimesForm': ReportCrimesForm}
    template_name = 'officers/update-incidents.html'

    
    def get(self, request, incident_id, *args, **kwargs):
        incident_obj = Incident.objects.get(id=incident_id)
        form = self.form_class["AccidentsForm"]() if incident_obj.incident_type == 'Road accident' else self.form_class["CrimesForm"]()
        incident_qs = Incident.objects.all()[:15]
        context = {
            'IncidentForm': form, 
            'incident_obj': incident_obj, 
            'reported_incidents': incident_qs,
        }
        return render(request, self.template_name, context)
    

    def post(self, request, incident_id, *args, **kwargs):
        incident_obj = Incident.objects.get(id=incident_id)
        form = self.form_class["AccidentsForm"](request.POST) if incident_obj.incident_type == 'Road accident' else self.form_class["CrimesForm"](request.POST)
        location_obj = IncidentLocation.objects.get(incident_id_id=incident_id)
        incident_qs = Incident.objects.all()[:15]

        
        if form.is_valid():
            new_record = form.save(commit=False)
            new_record.location_id = location_obj
            new_record.save()

            messages.success(request, 'Details submitted successfully!')

        context = {
            'IncidentForm': form, 
            'incident_obj': incident_obj,
            'reported_incidents': incident_qs,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: user.is_officer is True and user.is_roadsafetystaff is False and user.is_staff is False and user.is_superuser is False), name='get')
class WantedSuspectsCreateView(View):
    form_class = AddWantedSuspectsForm
    template_name = 'core/wanted-suspects.html'


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        suspects_qs = WantedSuspect.objects.all()

        context = {'WantedSuspectsForm': form, 'wanted_suspects': suspects_qs}
        return render(request, self.template_name, context)
    

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Suspect details successfully saved!')
            return redirect('wanted_suspects')

        context = {'WantedSuspectsForm': form}
        return render(request, self.template_name, context)

@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: user.is_officer is True and user.is_roadsafetystaff is False and user.is_staff is False and user.is_superuser is False), name='get')
class WantedSuspectsUpdateView(View):
    form_class = EditWantedSuspectsDetailsForm
    template_name = 'officers/edit-suspect.html'

    def get(self, request, suspect_id, *args, **kwargs):
        suspect_obj = WantedSuspect.objects.get(id=suspect_id)
        form = EditWantedSuspectsDetailsForm(instance=suspect_obj)

        context = {'EditSuspectDetailsForm': form, 'suspect': suspect_obj}
        return render(request, self.template_name, context)
    

    def post(self, request, suspect_id, *args, **kwargs):
        suspect_obj = WantedSuspect.objects.get(id=suspect_id)
        form = EditWantedSuspectsDetailsForm(request.POST, request.FILES, instance=suspect_obj)

        if form.is_valid():
            form.save()
            messages.warning(request, f"You updated suspect {suspect_obj.name}'s info!")
            return redirect('update_suspect', suspect_id)

        context = {'EditSuspectDetailsForm': form, 'suspect': suspect_obj}
        return render(request, self.template_name, context)