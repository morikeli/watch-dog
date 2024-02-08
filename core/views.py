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
