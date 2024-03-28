from django.utils.timesince import timesince
from django import template


register = template.Library()


@register.filter(name='datereported')
def incident_datetime_reported_filter(value):
    """ 
        This is function returns the time elapsed since an incident was reported. If the time elapsed is in: 
            - minutes, return 'm',
            - hours, return 'h', 
            - days, return 'd',
            - weeks, return 'w',
        
        If all the above conditions are false, i.e. time past is less than a minute, then return 'Just now'.
    """
    
    time_diff = timesince(value)   # time difference
    (time_diff := time_diff.split(',')[0])  # split time and access the first value.
    
    if 'minute' in time_diff:
        if int(time_diff[:1]) == 0:
            time_elapsed = f"Just now"
            return time_elapsed
        
        return f'{time_diff[:2]}mins ago' if int(time_diff[:2]) > 1 else f'{time_diff[:2]}min ago'
    
    elif 'hour' in time_diff:
        return f'{time_diff[:2]}hrs ago' if int(time_diff[:2]) > 1 else f'{time_diff[:2]}hr ago'
    
    elif 'day' in time_diff:
        return f'{time_diff[:2]}days ago' if int(time_diff[:2]) > 1 else f'{time_diff[:2]}day ago'
    
    elif 'week' in time_diff:
        return f'{time_diff[:2]}wks ago' if int(time_diff[:2]) > 1 else f'{time_diff[:2]}week ago'
    
    elif 'month' in time_diff:
        return f'{time_diff[:2]}mnths ago' if int(time_diff[:2]) > 1 else f'{time_diff[:2]}mnth ago'
    
    elif 'year' in time_diff:
        return f'{time_diff[:2]}yrs ago' if int(time_diff[:2]) > 1 else f'{time_diff[:2]}yr ago'
