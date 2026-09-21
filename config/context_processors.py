from notifications.models import Notification


def site_data(request):
    context = {"site_name": "College Smart Alumni"}
    if request.user.is_authenticated:
        context["unread_notification_count"] = Notification.objects.filter(
            user=request.user,
            is_read=False,
        ).count()
    return context
