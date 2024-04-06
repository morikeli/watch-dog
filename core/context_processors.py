from core.models import Notification


def notifications(request):
    user_notifications = Notification.objects.all().count()
    context = {'TotalNotifications': user_notifications}
    return context