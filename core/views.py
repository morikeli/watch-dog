from .forms import (
    AddWantedSuspectsForm, 
    EditWantedSuspectsDetailsForm,
    ReportIncidentForm, 
    ReportRoadAccidentForm, 
    ReportFireIncidentForm, 
    ReportCrimesForm, 
    ReportWantedSuspectForm,
    SubmitLocationForm, 
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.files.storage import FileSystemStorage
from django.utils.decorators import method_decorator
from formtools.wizard.views import SessionWizardView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.views import View
from .models import Incident, Location, RoadAccident, ReportedCrime, WantedSuspect
from folium.plugins import MarkerCluster, HeatMap
from sklearn.cluster import KMeans
import pandas as pd
import folium
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
        location_qs = Location.objects.all().order_by('-incident_id__date_reported')

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


@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False), name='get')
class GeoMapView(View):
    template_name = 'core/map.html'

    def get(self, request, *args, **kwargs):
        accident_spots = RoadAccident.objects.filter()

        # map config.
        map_figure = folium.Figure(height="800px")
        geo_map = folium.Map(
            location=[0.0236, 37.9062],     
            tiles='https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>',
            min_lat=0.0126,
            max_lat=5.2,
            zoom_start=7, 
            min_zoom=7,
            max_zoom=14,
            control_scale=True,
        ).add_to(map_figure)
        marker_cluster = MarkerCluster(name='Blackspots clusters').add_to(geo_map)

        for spot in accident_spots:     # get each record in the queryset
            lat_coord = 'S' if spot.location_id.latitude < 0 else 'N'
            popup_text = f"""
                <div class="table-responsive mt-3">
                    <table class="table table-sm table-hover table-striped table-condensed table-bordered">
                        <tbody>
                            <tr><td class="fw-bold">Coordinates</td><td>{ spot.location_id.latitude }&deg; {lat_coord}, { spot.location_id.longitude }&deg; E</td></tr>
                            <tr><td class="fw-bold">County</td><td>{ spot.location_id.county }</td></tr>
                            <tr><td class="fw-bold">Sub county</td><td>{ spot.location_id.sub_county }</td></tr>
                            <tr><td class="fw-bold">City/Place</td><td>{ spot.location_id.place }</td></tr>
                            <tr><td class="fw-bold">Road/Highway</td><td>{ spot.road }</td></tr>
                            <tr><td class="fw-bold">Road user/Victim</td><td>{ spot.road_user }</td></tr>
                            <tr><td class="fw-bold">Total injuries</td><td>{ spot.injuries_count }</td></tr>
                        </tbody>
                    </table>
                </div>
            """

            # markers
            folium.Marker(
                location=[spot.location_id.latitude, spot.location_id.longitude],
                tooltip='Click marker for more info.',
                popup=popup_text,
                icon=folium.Icon(icon='exclamation-triangle', color='red', prefix='fa', icon_color='#fffb00'),
            ).add_to(marker_cluster)
        
        heatmap_data = [[spot.location_id.latitude, spot.location_id.longitude] for spot in accident_spots]
        HeatMap(heatmap_data, name='Heat map', radius=20, show=False).add_to(geo_map)
        folium.LayerControl().add_to(geo_map)

        
        context = {
            'Map': geo_map._repr_html_,
            
        }
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
    template_name = 'core/edit-suspect.html'

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