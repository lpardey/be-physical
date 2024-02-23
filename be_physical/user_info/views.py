from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from pydantic import ValidationError

from .models import UserInfo
from .schemas import PhysicalBiometricsSchema, UserInfoSchema

# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, world. You're at the user_info index.")


@sync_to_async
@require_http_methods(["POST"])
def create(request: HttpRequest) -> JsonResponse:
    username = request.POST["username"]
    height = request.POST["height"]
    birth_date = request.POST["birth_date"]
    password = request.POST["password"]
    email = request.POST["email"]

    if User.objects.filter(username).exists():
        return JsonResponse({"Error": f"Username '{username}' already exists."}, status=400)

    user = User.objects.create_user(username, email, password, height, birth_date)
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
def get_physical_biometrics(request: HttpRequest) -> JsonResponse:
    user_info = get_object_or_404(UserInfo, user_id=request.GET["id"])
    weight_query = user_info.tracking_points.filter(label__label="weight").order_by("-date")
    weight_record = weight_query.values_list("value", flat=True).first()
    desired_weight_query = user_info.tracking_points.filter(label__label="desired_weight").order_by("-date")
    desired_weight_record = desired_weight_query.values_list("value", flat=True).first()
    data = PhysicalBiometricsSchema(
        height=user_info.height,
        weight=weight_record,
        desired_weight=desired_weight_record,
        bmi=user_info.bmi,
        bmi_category=user_info.category_name_by_bmi,
    )
    response = JsonResponse(data.model_dump())
    return response


async def get_tracking_points(request: HttpRequest) -> JsonResponse:
    ...


async def get_filtered_tracking_point(request: HttpRequest) -> JsonResponse:
    ...


async def get_annotations(request: HttpRequest) -> JsonResponse:
    ...


async def get_filtered_annotation(request: HttpRequest) -> JsonResponse:
    ...


async def create_tracking_point(request: HttpRequest) -> JsonResponse:
    ...


async def create_annotation(request: HttpRequest) -> JsonResponse:
    ...


async def get_streak(request: HttpRequest) -> JsonResponse:
    ...
