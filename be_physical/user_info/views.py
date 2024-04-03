import itertools

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import UserInfo
from .serializers import (
    AnnotationRequestSerializer,
    AnnotationsSerializer,
    BiometricsSerializer,
    CreateUserInfoRequestSerializer,
    GroupedTrackingPointsQueryParamsSerializer,
    TrackingLabelSerializer,
    TrackingPointRequestSerializer,
    TrackingPointsSerializer,
    UserInfoSerializer,
    serialize_grouped_tracking_groups,
    serialize_tracking_points_labels,
)

LABELS_QUERY_PARAM = "labels"


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_user_info(request: Request) -> Response:
    request_data = request.data.copy()
    request_data["user"] = request.user.id
    serializer = CreateUserInfoRequestSerializer(data=request_data)

    if serializer.is_valid():
        serializer.save()
        response_data = {"data": serializer.data}
        response = Response(response_data, status.HTTP_201_CREATED)
    else:
        response = Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
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
    serializer = GroupedTrackingPointsQueryParamsSerializer(data=request.query_params)

    if serializer.is_valid():
        selected_labels = serializer.validated_data["labels"]
        points = user_info.tracking_points.filter(label__label__in=selected_labels).order_by("label__label", "date")
        points_groups = itertools.groupby(points, key=lambda p: p.label.label)
        data_serialized = serialize_grouped_tracking_groups(points_groups)
        response = Response(data_serialized)
    else:
        response = Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_annotations(request: Request) -> Response:
    user_info = get_object_or_404(UserInfo, user=request.user)
    serializer = AnnotationsSerializer(user_info)
    response = Response(serializer.data)
    return response


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_tracking_point(request: Request) -> Response:
    request_data = request.data
    serializer = TrackingPointRequestSerializer(data=request_data)

    if serializer.is_valid():
        serializer.save()
        response_data = {"data": serializer.data}
        response = Response(response_data, status=status.HTTP_201_CREATED)
    else:
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return response


@api_view(["POST"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
