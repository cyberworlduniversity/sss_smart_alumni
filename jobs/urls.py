from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [

    path(
        "",
        views.job_list,
        name="job_list"
    ),

    path(
        "create/",
        views.create_job,
        name="create_job"
    ),

    path(
        "delete/<int:pk>/",
        views.delete_job,
        name="delete_job"
    ),

    path(
        "apply/<int:pk>/",
        views.apply_job,
        name="apply_job"
    ),

    path(
        "applications/",
        views.application_list,
        name="application_list"
    ),

    path(
        "applications/<int:pk>/",
        views.view_application,
        name="view_application"
    ),

    path(
        "applications/<int:pk>/accept/",
        views.accept_application,
        name="accept_application"
    ),

    path(
        "applications/<int:pk>/reject/",
        views.reject_application,
        name="reject_application"
    ),

    path(
        "applications/<int:pk>/delete/",
        views.delete_application,
        name="delete_application"
    ),
]