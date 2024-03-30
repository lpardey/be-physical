import itertools

# from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import User
from django.http import HttpRequest, QueryDict
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import UserInfo
from .serializers import (
    AnnotationRequestSerializer,
    AnnotationsSerializer,
    BiometricsSerializer,
    CreateUserInfoRequestSerializer,
    TrackingLabelSerializer,
    TrackingPointRequestSerializer,
    TrackingPointsSerializer,
    UserInfoSerializer,
    serialize_grouped_tracking_groups,
    serialize_tracking_points_labels,
)

LABELS_QUERY_PARAM = "labels"
# CLUSTER_QUERY_PARAM = "cluster"


# @api_view(["POST"])
# def create(request: Request) -> Response:
#     username = request.data.get("username")
#     password = request.data.get("password")
#     email = request.data.get("email")
#     height = request.data.get("height")
#     birth_date = request.data.get("birth_date")

#     if not all([username, password, email, height, birth_date]):
#         return Response({"Error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

#     hashed_password = make_password(password)
#     user, created = User.objects.get_or_create(username=username, email=email, password=hashed_password)

#     if created:
#         UserInfo.objects.create(user=user, height=height, birth_date=birth_date)
#         response = Response({"Success": "User created successfully"}, status=status.HTTP_201_CREATED)
#     else:
#         response = Response({"Error": f"Username '{username}' already exists."}, status=status.HTTP_400_BAD_REQUEST)

#     return response


@api_view(["POST"])
@permission_classes([IsAuthenticated | IsAdminUser])
def create_user_info(request: Request) -> Response:
    request_data = request.data.dict()
    request_data["user"] = request.user.id
    serializer = CreateUserInfoRequestSerializer(data=request_data)

    if serializer.is_valid():
        serializer.save()
        response_data = dict(data=serializer.data)
        response_data["data"].pop("user")
        response_status = status.HTTP_201_CREATED
    else:
        response_data = serializer.errors
        response_status = status.HTTP_400_BAD_REQUEST

    response = Response(response_data, response_status)

    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated | IsAdminUser])
def get_data(request: Request) -> Response:
    user_info = get_object_or_404(UserInfo, user=request.user)
    serializer = UserInfoSerializer(user_info)
    response = Response(serializer.data)
    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_biometrics(request: Request) -> Response:
    user_info = get_object_or_404(UserInfo, user=request.user)
    serializer = BiometricsSerializer(user_info)
    response = Response(serializer.data)
    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_tracking_points(request: Request) -> Response:
    """
    labels: list, starting_date: datetime, end_date: datetime
    {
        "tracking_ponts": [
            {"label": "push ups", "date": "2023-10-25", value: 6},
            {"label": "weight", "date": "2023-10-25", "value": 78.5},
        ]
    }
    """
    user_info = get_object_or_404(UserInfo, user=request.user)
    serializer = TrackingPointsSerializer(user_info)
    response = Response(serializer.data)
    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_grouped_tracking_points(request: Request) -> Response:
    """
    {
        "tracking_points": [
            {
                "label": "push ups",
                "values": [
                    {"date": "2023-10-23 (datetime)", "value": 5},
                    {"date": "2023-10-24", "value": 5},
                ],
            },
            {
                "label": "running",
                "values": [
                    {"date": "2024-10-23 (datetime)", "value": 5},
                    {"date": "2024-10-24", "value": 5},
                ],
            }
    ]
    }
    """
    user_info = get_object_or_404(UserInfo, user=request.user)
    query_params: QueryDict = request.query_params
    selected_labels = query_params.getlist(LABELS_QUERY_PARAM)
    points = user_info.tracking_points.filter(label__label__in=selected_labels).order_by("label__label", "date")
    points_groups = itertools.groupby(points, key=lambda p: p.label.label)
    data_serialized = serialize_grouped_tracking_groups(points_groups)
    response = Response(data_serialized)
    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_annotations(request: Request) -> Response:
    user_info = get_object_or_404(UserInfo, user=request.user)
    serializer = AnnotationsSerializer(user_info)
    response = Response(serializer.data)
    return response


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_grouped_annotations(request: Request) -> Response:
#     """
#     {
#         "annotations": [
#             {
#                 "annotation_type": 0,
#                 "values": [
#                     {"text": "my annotation 1", "scope": 0, "status":1},
#                     {"text": "my annotation 2", "scope": 0, "status":1},
#                 ],
#             },
#             {
#                 "annotation_type": 1,
#                 "values": [
#                     {"text": "trainer annotation 1", "scope": 1, "status":0},
#                     {"text": "trainer annotation 2", "scope": 1, "status":1},
#                 ],
#             },
#     ]
#     }
#     """
#     user_info = get_object_or_404(UserInfo, user=request.user)
#     query_params: QueryDict = request.query_params
#     selected_cluster = query_params.getlist(CLUSTER_QUERY_PARAM, default=["annotation_type"])
#     annotations = user_info.annotations.filter(selected_cluster[0]__in=selected_cluster).order_by(f"{selected_cluster[0]}", "date")
#     return


@api_view(["POST"])
@permission_classes([IsAuthenticated | IsAdminUser])
def create_tracking_point(request: Request) -> Response:
    request_data = request.data
    serializer = TrackingPointRequestSerializer(data=request_data)

    if serializer.is_valid():
        serializer.save()
        response_data = dict(data=serializer.data)
        response = Response(response_data, status=status.HTTP_201_CREATED)
    else:
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return response


@api_view(["POST"])
@permission_classes([IsAuthenticated | IsAdminUser])
def create_annotation(request: Request) -> Response:
    request_data = request.data
    serializer = AnnotationRequestSerializer(data=request_data)

    if serializer.is_valid():
        serializer.save()
        response_data = dict(data=serializer.data)
        response = Response(response_data, status=status.HTTP_201_CREATED)
    else:
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return response


@api_view(["POST"])
@permission_classes([IsAuthenticated | IsAdminUser])
def create_tracking_label(request: Request) -> Response:
    request_data = request.data
    serializer = TrackingLabelSerializer(data=request_data)

    if serializer.is_valid():
        serializer.save()
        response_data = dict(data=serializer.data)
        response = Response(response_data, status=status.HTTP_201_CREATED)
    else:
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_tracking_points_labels(request: Request) -> Response:
    """
    {
        "tracking_points_labels":
        [
            {
                "label": "label_1":
                "description": "description_1"
            },
            {
                "label": "label_2":
                "description": "description_2"
            },
            {
                "label": "label_3":
                "description": "description_3"
            },
        ]
    }
    """
    user_info = get_object_or_404(UserInfo, user=request.user)
    tracking_points = user_info.tracking_points.select_related("label")
    labels = {point.label for point in tracking_points}
    data_serialized = serialize_tracking_points_labels(labels)
    response = Response(data_serialized)
    return response


def get_streak(request: HttpRequest) -> None:
    return
