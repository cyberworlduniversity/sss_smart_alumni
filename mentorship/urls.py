from django.urls import path

from . import views

urlpatterns = [
    path("", views.mentorship_list, name="mentorship_list"),
    path("request/<int:alumni_id>/", views.request_mentorship, name="request_mentorship"),
    path("accept/<int:pk>/", views.accept_mentorship, name="accept_mentorship"),
    path("reject/<int:pk>/", views.reject_mentorship, name="reject_mentorship"),
]
