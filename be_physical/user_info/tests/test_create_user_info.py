import datetime

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from ..models import UserInfo
from ..urls import CREATE_USER_INFO_VIEW_NAME, app_name
from .conftest import UNAUTHORIZED_RESPONSE, APIClient


@pytest.mark.django_db
@pytest.mark.parametrize("user_fixture", ["user", "admin_user", "superuser"], indirect=True)
def test_create_successful(user_fixture: User, api_client: APIClient):
    api_client.force_authenticate(user_fixture)
    data = {"height": "1.90", "birth_date": "1989-09-01"}
    expected_response = {"data": data}
    url = reverse(f"{app_name}:{CREATE_USER_INFO_VIEW_NAME}")

    response: Response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_response
    assert UserInfo.objects.filter(user=user_fixture).exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "height, birth_date",
    [
        pytest.param("invalid_height", "1989-09-01", id="Invalid height type"),
        pytest.param("1.7563", "1989-09-01", id="Height with more than two decimal values"),
        pytest.param("2.51", "1989-09-01", id="Height value out of upper bound"),
        pytest.param("0.99", "1989-09-01", id="Height value out of lower bound"),
        pytest.param("", "1989-09-01", id="Missing height"),
        pytest.param("2.00", "invalid_date", id="Invalid date type"),
        pytest.param("2.00", datetime.date.today(), id="Birth date out of upper bound"),
        pytest.param("2.00", "1922-09-01", id="Birth date out of lower bound"),
        pytest.param("2.00", "", id="Missing date"),
    ],
)
def test_create_user_info_bad_request(height: str, birth_date: str, api_client_authenticated: APIClient):
    data = {"height": height, "birth_date": birth_date}
    url = reverse(f"{app_name}:{CREATE_USER_INFO_VIEW_NAME}")

    response: Response = api_client_authenticated.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_unauthorized_user(api_client: APIClient):
    url = reverse(f"{app_name}:{CREATE_USER_INFO_VIEW_NAME}")

    response: Response = api_client.post(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == UNAUTHORIZED_RESPONSE


@pytest.mark.django_db
def test_user_already_exists(api_client_authenticated: APIClient, user: User, basic_user_info: UserInfo):
    data = {"height": "1.35", "birth_date": "1989-09-01"}
    url = reverse(f"{app_name}:{CREATE_USER_INFO_VIEW_NAME}")

    response: Response = api_client_authenticated.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.parametrize("http_method", ["get", "put", "patch", "delete"])
def test_create_user_info_incorrect_http_method(http_method: str, api_client_authenticated: APIClient):
    url = reverse(f"{app_name}:{CREATE_USER_INFO_VIEW_NAME}")
    request_method = getattr(api_client_authenticated, http_method)

    response: Response = request_method(url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
