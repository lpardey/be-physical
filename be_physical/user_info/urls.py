from django.urls import path

from . import views

app_name = "user_info"
urlpatterns = [
    path("", views.index, name="index"),
    path("data/", views.get_data, name="user_info_data"),
    path("biometrics/", views.get_biometrics, name="biometrics"),
    path("tracking_points", views.get_tracking_points, name="tracking_points"),
    path("annotations/", views.get_annotations, name="annotations"),
    path("create/", views.create, name="create"),
]

# GET /users/{id}: Retrieve user information by user ID.
# GET /users/{id}/biometrics: Retrieve physical biometrics data for a user.
# POST /users: Create a new user in the database.
