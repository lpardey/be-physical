from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from .models import UserInfo
from .serializers import (
    AnnotationsData,
    AnnotationSerializer,
    BiometricsSerializer,
    TrackingPointsSerializer,
    UserInfoSerializer,
)

# Create your views here.


@api_view(["GET"])
def index(request: Request) -> JsonResponse:
    return JsonResponse("Hello, world. You're at the user_info index.")


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
    user_info = get_object_or_404(UserInfo, user=request.user)
    serializer = TrackingPointsSerializer(user_info)
    response = JsonResponse(serializer.data)
    return response


def get_tracking_points_by_filter(request: HttpRequest) -> JsonResponse:
    ...


@require_http_methods(["GET"])
def get_annotations(request: HttpRequest) -> JsonResponse:
    user_info = get_object_or_404(UserInfo, user_id=request.GET["id"])
    annotations = [AnnotationSerializer(**annotation) for annotation in user_info.annotations.values()]
    data = AnnotationsData(annotations=annotations)
    response = JsonResponse(data.model_dump())
    return response


def get_annotations_by_filter(request: HttpRequest) -> JsonResponse:
    ...


def create_tracking_point(request: HttpRequest) -> JsonResponse:
    ...


def create_annotation(request: HttpRequest) -> JsonResponse:
    ...


def get_streak(request: HttpRequest) -> JsonResponse:
    ...
