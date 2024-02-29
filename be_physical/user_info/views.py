from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
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
    TrackingPointsData,
    TrackingPointSerializer,
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


@require_http_methods(["GET"])
def get_biometrics(request: HttpRequest) -> JsonResponse:
    user_info = get_object_or_404(UserInfo, user_id=request.GET["id"])
    weight_filter = user_info.tracking_points.filter(label__label="weight").order_by("-date")
    desired_weight_filter = user_info.tracking_points.filter(label__label="desired_weight").order_by("-date")
    data = BiometricsSerializer(
        height=user_info.height,
        weight=weight_filter.values_list("value", flat=True).first(),
        desired_weight=desired_weight_filter.values_list("value", flat=True).first(),
        bmi=user_info.bmi,
        bmi_category=user_info.category_name_by_bmi,
    )
    response = JsonResponse(data)
    return response


@require_http_methods(["GET"])
def get_tracking_points(request: HttpRequest) -> JsonResponse:
    user_info = get_object_or_404(UserInfo, user_id=request.GET["id"])
    tracking_points = [
        TrackingPointSerializer(
            label=point.label.label,
            description=point.label.description,
            date=point.date,
            value=point.value,
        )
        for point in user_info.tracking_points.all()
    ]
    data = TrackingPointsData(tracking_points=tracking_points)
    response = JsonResponse(data.model_dump())
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
