from .models import (
    Incident, 
    Location, 
    RoadAccident, 
    FireIncident, 
    ReportedCrime, 
    PoliceStation, 
    WantedSuspect, 
    ReportSuspect, 
    Notification
)
from django.db.models.signals import pre_save, post_save
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


@receiver(pre_save, sender=ReportSuspect)
def generate_reported_suspectID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4().hex)[:30]


@receiver(pre_save, sender=Notification)
def generate_notificationID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4().hex)[:30]


@receiver(post_save, sender=Location)
def send_reported_incident_notification(sender, instance, created, **kwargs):
    if created:
        notify = Notification.objects.create(
            incident_location=instance,
            notification_type=1,
        )
        notify.save()


@receiver(post_save, sender=WantedSuspect)
def send_wanted_suspect_notification(sender, instance, created, **kwargs):
    if created:
        notify = Notification.objects.create(
            wanted_suspect=instance,
            notification_type=2,
        )
        notify.save()


@receiver(post_save, sender=ReportSuspect)
def send_notification_for_wanted_suspect(sender, instance, created, **kwargs):
    if created:
        notify = Notification.objects.create(
            suspect=instance,
            notification_type=3,
        )
        notify.save()