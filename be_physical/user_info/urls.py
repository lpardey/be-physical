from django.urls import path

from . import views

app_name = "user_info"

CREATE_USER_INFO_VIEW_NAME = "user_info_create"
GET_DATA_VIEW_NAME = "user_info_data"
GET_BIOMETRICS_VIEW_NAME = "user_info_biometrics"
GET_TRACKING_POINTS_VIEW_NAME = "user_info_tracking_points"
CREATE_TRACKING_POINT_VIEW_NAME = "user_info_create_tracking_point"
GET_TRACKING_POINTS_LABELS_VIEW_NAME = "user_info_tracking_points_labels"
CREATE_TRACKING_LABEL_VIEW_NAME = "user_info_tracking_label"
GET_GROUPED_TRACKING_POINTS_VIEW_NAME = "user_info_grouped_tracking_points"
GET_ANNOTATIONS_VIEW_NAME = "user_info_annotations"
CREATE_ANNOTATION_VIEW_NAME = "user_info_create_annotation"

urlpatterns = [
    path("create/", views.create_user_info, name=CREATE_USER_INFO_VIEW_NAME),
    path("data/", views.get_data, name=GET_DATA_VIEW_NAME),
    path("biometrics/", views.get_biometrics, name=GET_BIOMETRICS_VIEW_NAME),
    path("tracking_points/", views.get_tracking_points, name=GET_TRACKING_POINTS_VIEW_NAME),
    path("tracking_points/create/", views.create_tracking_point, name=CREATE_TRACKING_POINT_VIEW_NAME),
    path("tracking_points/labels/", views.get_tracking_points_labels, name=GET_TRACKING_POINTS_LABELS_VIEW_NAME),
    path("tracking_points/labels/create/", views.create_tracking_label, name=CREATE_TRACKING_LABEL_VIEW_NAME),
    path(
        "grouped_tracking_points/",
        views.get_grouped_tracking_points,
        name=GET_GROUPED_TRACKING_POINTS_VIEW_NAME,
    ),
    path("annotations/", views.get_annotations, name=GET_ANNOTATIONS_VIEW_NAME),
    path("annotations/create/", views.create_annotation, name=CREATE_ANNOTATION_VIEW_NAME),
]
