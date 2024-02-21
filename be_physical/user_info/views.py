from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseNotFound, JsonResponse
from django.views.decorators.http import require_http_methods

from .models import UserInfo

# Create your views here.


@require_http_methods(["GET"])
@login_required
async def get_data(request: HttpRequest) -> JsonResponse:
    """All user data in user info such as: id, username, creation date, birthdate, etc"""
    user_info = UserInfo.objects.filter(user__id=request.user.id).first()

    if user_info is None:
        return HttpResponseNotFound("User information not found")

    data = {
        "username": user_info.user.username,
        "email": user_info.user.email,
        "birth_date": user_info.birth_date,
        "creation_date": user_info.user.date_joined,
    }
    response = JsonResponse(data)

    return response


async def get_physical_biometrics(request: HttpRequest) -> JsonResponse:
    """User physical biometrics such as: weight, desired weight, height, bmi, bmi category, etc."""
    ...


async def get_tracking_points(request: HttpRequest) -> JsonResponse:
    ...


async def get_tracking_point_by_factory(request: HttpRequest) -> JsonResponse:
    ...


async def get_annotations(request: HttpRequest) -> JsonResponse:
    ...


async def get_user_annotation_by_factory(request: HttpRequest) -> JsonResponse:
    ...


async def create_user(request: HttpRequest) -> JsonResponse:
    ...


async def create_user_tracking_point(request: HttpRequest) -> JsonResponse:
    ...


async def create_user_annotation(request: HttpRequest) -> JsonResponse:
    ...
