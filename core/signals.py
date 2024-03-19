from .models import Incident, Location, RoadAccident, FireIncident, ReportedCrime, PoliceStation, WantedSuspect
from django.db.models.signals import pre_save
from django.dispatch import receiver
import uuid


@receiver(pre_save, sender=Incident)
def generate_incidentsID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4().hex)[:30]


@receiver(pre_save, sender=Location)
def generate_locationID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4().hex)[:30]


@receiver(pre_save, sender=RoadAccident)
def generate_road_accidentsID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4().hex)[:30]


@receiver(pre_save, sender=FireIncident)
def generate_fire_incidentID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4().hex)[:30]


@receiver(pre_save, sender=ReportedCrime)
def generate_reported_crimesID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4().hex)[:30]


@receiver(pre_save, sender=PoliceStation)
def generate_police_stationID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4().hex)[:30]


@receiver(pre_save, sender=WantedSuspect)
def generate_wanted_suspectID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4().hex)[:30]