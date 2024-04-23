from core.models import Notification


def notifications(request):
    user_notifications = Notification.objects.all().count()

    # users can't see notifications for reported wanted suspects
    # to display total notifications, subtract 'reported wanted suspects' notifications
    # from total notifications

    if request.user.is_authenticated and request.user.is_officer is True:   # First, check if the user is authenticated or it will generate an AttributError.
        pass
    else:
        wanted_suspects_notifs = Notification.objects.filter(notification_type=3).count()
        user_notifications = user_notifications - wanted_suspects_notifs
    
    context = {'TotalNotifications': user_notifications}
    return context