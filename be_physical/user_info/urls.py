from django.urls import path

from . import views

app_name = "user_info"
urlpatterns = [
    path("", views.index, name="index"),
    path("data/", views.get_data, name="user_info_data"),
    path("physical_biometrics/", views.get_physical_biometrics, name="physical_biometrics"),
    path("create/", views.create, name="create"),
]
