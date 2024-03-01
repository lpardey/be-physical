from django.urls import path

from . import views

app_name = "user_info"

GET_DATA_VIEW_NAME = "user_info_data"
GET_BIOMETRICS_VIEW_NAME = "user_info_biometrics"
GET_TRACKING_POINTS_VIEW_NAME = "user_info_tracking_points"
GET_ANNOTATIONS_VIEW_NAME = "user_info_annotations"
CREATE_VIEW_NAME = "user_info_create"

urlpatterns = [
    path("data/", views.get_data, name=GET_DATA_VIEW_NAME),
    path("biometrics/", views.get_biometrics, name=GET_BIOMETRICS_VIEW_NAME),
    path("tracking_points/", views.get_tracking_points, name=GET_TRACKING_POINTS_VIEW_NAME),
    path("annotations/", views.get_annotations, name=GET_ANNOTATIONS_VIEW_NAME),
    path("create/", views.create, name=CREATE_VIEW_NAME),
]

# GET /users/{id}: Retrieve user information by user ID.
# GET /users/{id}/biometrics: Retrieve physical biometrics data for a user.
# POST /users: Create a new user in the database.
