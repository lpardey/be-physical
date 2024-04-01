from typing import Any
from unittest.mock import Mock, patch

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from ..models import UserInfo
from ..serializers import UserInfoSerializer
from ..urls import GET_DATA_VIEW_NAME, app_name
from .conftest import (
    PERMISSION_DENIED_RESPONSE,
    UNAUTHORIZED_RESPONSE,
    USER_INFO_NOT_FOUND_RESPONSE,
)


@pytest.mark.django_db
@pytest.mark.parametrize("user_fixture", ["user", "admin_user", "superuser"], indirect=True)
def test_get_data_success(user_fixture: User, user_info_fixture: UserInfo, api_client: APIClient):
    api_client.force_authenticate(user_fixture)
    expected_response = UserInfoSerializer(user_info_fixture).data
    url = reverse(f"{app_name}:{GET_DATA_VIEW_NAME}")

    response: Response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


@pytest.mark.django_db
@patch("user_info.views.get_object_or_404")
def test_get_data_for_other_user(m_get_object_or_404: Mock, user: User, api_client_authenticated: APIClient):
    assert not user.is_staff
    assert not user.is_superuser

    target_user = User.objects.create(username="target_user", email="target_user@example.com", password="12345")
    target_user_info = UserInfo.objects.create(user=target_user, height="1.80", birth_date="1990-01-01")
    m_get_object_or_404.return_value = target_user_info
    url = reverse(f"{app_name}:{GET_DATA_VIEW_NAME}")

    response: Response = api_client_authenticated.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == PERMISSION_DENIED_RESPONSE


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_response",
    [
        pytest.param(
            "api_client",
            status.HTTP_401_UNAUTHORIZED,
            UNAUTHORIZED_RESPONSE,
            id="Unauthorized",
        ),
        pytest.param(
            "api_client_authenticated",
            status.HTTP_404_NOT_FOUND,
            USER_INFO_NOT_FOUND_RESPONSE,
            id="UserInfo not found",
        ),
    ],
    indirect=["client_fixture"],
)
@pytest.mark.django_db
def test_get_data_failed(client_fixture: APIClient, expected_status: status, expected_response: dict[str, Any]):
    url = reverse(f"{app_name}:{GET_DATA_VIEW_NAME}")

    response: Response = client_fixture.get(url)

    assert response.status_code == expected_status
    assert response.json() == expected_response


@pytest.mark.django_db
@pytest.mark.parametrize("http_method", ["post", "put", "patch", "delete"])
def test_get_data_incorrect_http_method(http_method: str, api_client_authenticated: APIClient):
    url = reverse(f"{app_name}:{GET_DATA_VIEW_NAME}")
    request_method = getattr(api_client_authenticated, http_method)

    response: Response = request_method(url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
