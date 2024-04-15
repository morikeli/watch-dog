from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_incident_date(value):
    """
    This function validates date provided in the input field `incident_date` in `ReportIncidentForm`.
    Users cannot reported incidents that is past one week, i.e. occured more than a week ago (more than 7 days).
    """
    current_dt = timezone.now().date()
    days_elapsed = current_dt - value

    if value > current_dt:
        raise ValidationError(f'Invalid date provided! Current date is "{current_dt}"')
    
    if days_elapsed.days > 7:
        raise ValidationError("You can't report an incident that is past 1 week! Report the incident to the nearest police station.")


def validate_incident_time(value):
    """
    This function validates time provided in the input field `incident_time` in `ReportIncidentForm`.
    Users cannot provide timestamp when reporting incidents that is greater than the current time.
    """

    current_time = timezone.now() + timezone.timedelta(hours=3)
    current_time_str = timezone.now().time().strftime("%H:%M:%S")

    if value > current_time.time():
        raise ValidationError(f'Invalid time provided! Current time is "{current_time_str}"')


def validate_last_seen_date(request):
    """ 
    This function is used to validate date provided in `last_seen_date` input field in `ReportWantedSuspectsForm`.
    The function validates if the user has provided a date that is greater than the current date. 
    """

    current_date = timezone.datetime.now().strftime('%Y-%m-%d')
    last_seen_date = request.POST.get('last_seen_date')

    if last_seen_date > timezone.datetime.now().strftime('%Y-%m-%d'):
        return HttpResponse(f'<div class="error mt-1">Invalid date provided. Today is <b>{current_date}</b> but you provided date {last_seen_date}.</div>')

    return HttpResponse()


def validate_last_seen_time(request):
    """ 
    This function is used to validate time provided in `last_seen_time` input field in `ReportWantedSuspectsForm`.
    The function validates if the user has provided time that is greater than the current time. 
    """

    current_time = timezone.datetime.now().hour + 3, timezone.datetime.now().minute, timezone.datetime.now().second
    last_seen_time = request.POST.get('last_seen_time')
    
    if last_seen_time > f'{current_time[0]}:{current_time[1]}':
        return HttpResponse(
            f"""<div class="error">
                Invalid time provided. Current time: <b>{current_time[0]:02d}:{current_time[1]:02d}</b> but you provided "{last_seen_time}"
            </div>"""
        )
    
    return HttpResponse()