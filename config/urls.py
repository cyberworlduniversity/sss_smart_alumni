from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Main entry page: index.html is the login page.
    path(
        "",
        auth_views.LoginView.as_view(
            template_name="index.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),

    path("accounts/", include("accounts.urls")),
    path("jobs/", include("jobs.urls")),
    path("alumni/", include("alumni.urls")),
    path("students/", include("students.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("mentorship/", include("mentorship.urls")),
    path("post_list/", include("forum.urls")),
    path("notifications/", include("notifications.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
