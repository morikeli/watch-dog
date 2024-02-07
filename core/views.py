from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .forms import ReportIncidentForm, SubmitLocationForm, ReportRoadAccidentForm, ReportFireIncidentForm, ReportCrimesForm


class HomepageView(View):
    template_name = 'core/homepage.html'

    def get(self, request, *args, **kwargs):

        context = {}
        return render(request, self.template_name, context)
