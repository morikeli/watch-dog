from .forms import ReportIncidentForm, SubmitLocationForm, ReportRoadAccidentForm, ReportFireIncidentForm, ReportCrimesForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Incident, Location, RoadAccident, ReportedCrime
from folium.plugins import MarkerCluster
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
                <div></div>
                <div class="table-responsive mt-3">
                    <table class="table table-sm table-hover table-striped table-condensed table-bordered">
                        <tbody>
                            <tr><td class="fw-bold">Coordinates</td><td>{ spot.location_id.latitude }&deg; {lat_coord}, { spot.location_id.longitude }&deg; E</td></tr>
                            <tr><td class="fw-bold">County</td><td>{ spot.location_id.county }</td></tr>
                            <tr><td class="fw-bold">Sub county</td><td>{ spot.location_id.sub_county }</td></tr>
                            <tr><td class="fw-bold">City/Place</td><td>{ spot.location_id.city }</td></tr>
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
        
        folium.LayerControl().add_to(geo_map)

        
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


@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False), name='get')
class ReportIncidentsView(View):
    template_name = 'core/report-incident.html'

    
    def get(self, request, *args, **kwargs):

        context = {}
        return render(request, self.template_name, context)
    

    def post(self, request, *args, **kwargs):

        context = {}
        return render(request, self.template_name, context)