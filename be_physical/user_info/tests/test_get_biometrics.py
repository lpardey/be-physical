from typing import Any

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from ..models import UserInfo
from ..serializers import BiometricsSerializer
from ..urls import GET_BIOMETRICS_VIEW_NAME, app_name
from .generic_test_http_methods import GenericTestIncorrectHTTPMethods


@pytest.mark.django_db
def test_get_biometrics_success(api_client_authenticated: APIClient, user_info_fixture: UserInfo):
    expected_response = BiometricsSerializer(user_info_fixture).data
    url = reverse(f"{app_name}:{GET_BIOMETRICS_VIEW_NAME}")

    response: Response = api_client_authenticated.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_response_fixture",
    [
        pytest.param(
            "api_client",
            status.HTTP_401_UNAUTHORIZED,
            "unauthorized_response",
            id="Unauthorized",
        ),
        pytest.param(
            "api_client_authenticated",
            status.HTTP_404_NOT_FOUND,
            "user_info_not_found_response",
            id="UserInfo not found",
        ),
    ],
    indirect=["client_fixture", "expected_response_fixture"],
)
def test_get_biometrics_failed(
    client_fixture: APIClient, expected_status: status, expected_response_fixture: dict[str, Any]
):
    url = reverse(f"{app_name}:{GET_BIOMETRICS_VIEW_NAME}")

    response: Response = client_fixture.get(url)

    assert response.status_code == expected_status
    assert response.json() == expected_response_fixture


@pytest.mark.django_db
class TestGetBiometricsIncorrectHTTPMethods(GenericTestIncorrectHTTPMethods):
    VIEW_NAME = GET_BIOMETRICS_VIEW_NAME
    ALLOWED_METHODS = ["get"]
