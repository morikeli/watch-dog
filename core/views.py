from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .forms import ReportIncidentForm, SubmitLocationForm, ReportRoadAccidentForm, ReportFireIncidentForm, ReportCrimesForm
import folium


@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False), name='get')
class HomepageView(View):
    template_name = 'core/homepage.html'

    def get(self, request, *args, **kwargs):

        context = {}
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False), name='get')
class GeoMapView(View):
    template_name = 'core/map.html'

    def get(self, request, *args, **kwargs):
        map_figure = folium.Figure(height="800px")
        geo_map = folium.Map(
            location=[0.0236, 37.9062],     
            tiles='https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>',
            min_lat=0.0126,
            max_lat=5.2,
            control_scale=True, 
            zoom_start=7, 
            min_zoom=7,
            max_zoom=14,
        ).add_to(map_figure)
        
        context = {
            'Map': geo_map._repr_html_,
            
        }
        return render(request, self.template_name, context)
    

@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False), name='get')
class IncidentsStatisticsView(View):
    template_name = 'core/incidents.html'

    def get(self, request, *args, **kwargs):
        

        context = {}
        return render(request, self.template_name, context)

