from django.http import HttpResponse
from django.utils import timezone


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