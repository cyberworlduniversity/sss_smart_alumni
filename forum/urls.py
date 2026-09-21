from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("create/", views.create_post, name="create_post"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path("delete/<int:pk>/", views.delete_post, name="delete_post"),
]