import itertools

from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse, QueryDict
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from .models import UserInfo
from .serializers import (
    # AnnotationSerializer,
    BiometricsSerializer,
    # GroupedTrackingPointSerializer,
    TrackingPointsSerializer,
    UserInfoSerializer,
    serialize_grouped_tracking_groups,
)

LABELS_QUERY_PARAM = "labels"


@api_view(["POST"])
def create(request: Request) -> JsonResponse:
    username = request.POST["username"]
    user, created = User.objects.get_or_create(username=username, defaults=request.POST)

    if created:
        return JsonResponse({"Success": "User created successfully"}, status=status.HTTP_201_CREATED)

    return JsonResponse({"Error": f"Username '{username}' already exists."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_data(request: Request) -> JsonResponse:
    user_info = get_object_or_404(UserInfo, user=request.user)
    serializer = UserInfoSerializer(user_info)
    response = JsonResponse(serializer.data)
    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_biometrics(request: Request) -> JsonResponse:
    user_info = get_object_or_404(UserInfo, user=request.user)
    serializer = BiometricsSerializer(user_info)
    response = JsonResponse(serializer.data)
    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_tracking_points(request: Request) -> JsonResponse:
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
    response = JsonResponse(serializer.data)
    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_grouped_tracking_points(request: Request) -> JsonResponse:
    """
    {
        "tracking_ponts": [
            {
                "label": "push ups",
                "values": [
                    {"date": "2023-10-23 (datetime)", "value": 5},
                    {"date": "2023-10-24", "value": 5},
                ],
            }
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
    # serializer = GroupedTrackingPointsSerializer(points_groups)
    response = JsonResponse(data_serialized)
    return response


def get_annotations_by_filter(request: HttpRequest) -> None:
    return


def create_tracking_point(request: HttpRequest) -> None:
    return


def create_annotation(request: HttpRequest) -> None:
    return


def get_streak(request: HttpRequest) -> None:
    return


def create_label() -> None:
    return


def get_labels() -> None:
    return
