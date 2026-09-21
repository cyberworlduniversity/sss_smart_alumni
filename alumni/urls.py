from django.urls import path
from . import views

urlpatterns = [
    path("", views.alumni_list, name="alumni_list"),
    path("<int:pk>/", views.alumni_detail, name="alumni_detail"),
]
