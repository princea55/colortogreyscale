from django.urls import path
from . import views
urlpatterns = [
    path("", views.simple_upload, name="upload"),
    path("single-photo", views.single_file_photo, name="single_photo"),

]