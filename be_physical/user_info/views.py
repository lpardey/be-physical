from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from pydantic import ValidationError

from .models import UserInfo
from .schemas import (
    AnnotationSchema,
    AnnotationsData,
    BiometricsSchema,
    TrackingPointSchema,
    TrackingPointsData,
    UserInfoSchema,
)

# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, world. You're at the user_info index.")


@sync_to_async
@require_http_methods(["POST"])
def create(request: HttpRequest) -> JsonResponse:
    username = request.POST["username"]

    if User.objects.filter(username).exists():
        return JsonResponse({"Error": f"Username '{username}' already exists."}, status=400)

    user = User.objects.create_user(**request.POST)
    user.save()
    return JsonResponse({"Success": "User created successfully"})


@sync_to_async
@require_http_methods(["GET"])
def get_data(request: HttpRequest) -> JsonResponse:
    user_info = get_object_or_404(UserInfo, user_id=request.GET["id"])
    data = UserInfoSchema(
        username=user_info.user.username,
        email=user_info.user.email,
        birth_date=user_info.birth_date,
        creation_date=user_info.user.date_joined.date(),
    )
    response = JsonResponse(data.model_dump())
    return response


@sync_to_async
@require_http_methods(["GET"])
def get_biometrics(request: HttpRequest) -> JsonResponse:
    user_info = get_object_or_404(UserInfo, user_id=request.GET["id"])
    weight_filter = user_info.tracking_points.filter(label__label="weight").order_by("-date")
    desired_weight_filter = user_info.tracking_points.filter(label__label="desired_weight").order_by("-date")
    data = BiometricsSchema(
        height=user_info.height,
        weight=weight_filter.values_list("value", flat=True).first(),
        desired_weight=desired_weight_filter.values_list("value", flat=True).first(),
        bmi=user_info.bmi,
        bmi_category=user_info.category_name_by_bmi,
    )
    response = JsonResponse(data.model_dump())
    return response


@sync_to_async
@require_http_methods(["GET"])
def get_tracking_points(request: HttpRequest) -> JsonResponse:
    user_info = get_object_or_404(UserInfo, user_id=request.GET["id"])
    tracking_points = [
        TrackingPointSchema(
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


async def get_tracking_points_by_filter(request: HttpRequest) -> JsonResponse:
    ...


@sync_to_async
@require_http_methods(["GET"])
def get_annotations(request: HttpRequest) -> JsonResponse:
    user_info = get_object_or_404(UserInfo, user_id=request.GET["id"])
    annotations = [AnnotationSchema(**annotation) for annotation in user_info.annotations.values()]
    data = AnnotationsData(annotations=annotations)
    response = JsonResponse(data.model_dump())
    return response


async def get_annotations_by_filter(request: HttpRequest) -> JsonResponse:
    ...


async def create_tracking_point(request: HttpRequest) -> JsonResponse:
    ...


async def create_annotation(request: HttpRequest) -> JsonResponse:
    ...


async def get_streak(request: HttpRequest) -> JsonResponse:
    ...
