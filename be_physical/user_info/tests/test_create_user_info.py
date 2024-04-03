import datetime

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from ..models import UserInfo
from ..urls import CREATE_USER_INFO_VIEW_NAME, app_name
from .conftest import UNAUTHORIZED_RESPONSE, APIClient
from .generic_requests import CreateUserInfoRequest
from .generic_test_http_methods import GenericTestIncorrectHTTPMethods


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view_request, expected_status",
    [
        pytest.param(CreateUserInfoRequest(), status.HTTP_201_CREATED, id="Valid request"),
        pytest.param(CreateUserInfoRequest("invalid_height"), status.HTTP_400_BAD_REQUEST, id="Invalid height type"),
        pytest.param(
            CreateUserInfoRequest("1.7563"), status.HTTP_400_BAD_REQUEST, id="Height with more than two decimal values"
        ),
        pytest.param(CreateUserInfoRequest("2.51"), status.HTTP_400_BAD_REQUEST, id="Height value out of upper bound"),
        pytest.param(CreateUserInfoRequest("0.99"), status.HTTP_400_BAD_REQUEST, id="Height value out of lower bound"),
        pytest.param(CreateUserInfoRequest(""), status.HTTP_400_BAD_REQUEST, id="Missing height"),
        pytest.param(CreateUserInfoRequest("invalid_date"), status.HTTP_400_BAD_REQUEST, id="Invalid date type"),
        pytest.param(
            CreateUserInfoRequest(datetime.date.today()), status.HTTP_400_BAD_REQUEST, id="Date out of upper bound"
        ),
        pytest.param(CreateUserInfoRequest("1922-09-01"), status.HTTP_400_BAD_REQUEST, id="Date out of lower bound"),
        pytest.param(CreateUserInfoRequest(""), status.HTTP_400_BAD_REQUEST, id="Missing date"),
    ],
)
def test_create_user_info_success(
    view_request: CreateUserInfoRequest,
    expected_status: status,
    user: User,
    api_client_authenticated: APIClient,
):
    request_data = view_request.generate_data(user)
    url = reverse(f"{app_name}:{CREATE_USER_INFO_VIEW_NAME}")

    response: Response = api_client_authenticated.post(url, request_data)

    assert response.status_code == expected_status
    if expected_status == status.HTTP_201_CREATED:
        expected_response = {"data": request_data}
        assert response.json() == expected_response
        assert UserInfo.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_create_user_info_already_exists(basic_user_info: UserInfo, api_client_authenticated: APIClient):
    request_data = {"height": "1.90", "birth_date": "1989-09-01"}
    url = reverse(f"{app_name}:{CREATE_USER_INFO_VIEW_NAME}")

    response: Response = api_client_authenticated.post(url, request_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_user_info_unauthorized(api_client: APIClient):
    url = reverse(f"{app_name}:{CREATE_USER_INFO_VIEW_NAME}")

    response: Response = api_client.post(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == UNAUTHORIZED_RESPONSE


@pytest.mark.django_db
class TestGetCreateUserInfoIncorrectHTTPMethods(GenericTestIncorrectHTTPMethods):
    VIEW_NAME = CREATE_USER_INFO_VIEW_NAME
    ALLOWED_METHODS = ["post"]
