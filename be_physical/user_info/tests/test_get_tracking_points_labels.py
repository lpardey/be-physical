from typing import Any

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from ..models import UserInfo
from ..urls import GET_TRACKING_POINTS_LABELS_VIEW_NAME, app_name
from .conftest import UNAUTHORIZED_RESPONSE, USER_INFO_NOT_FOUND_RESPONSE
from .generic_test_http_methods import GenericTestIncorrectHTTPMethods


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_info_fixture, expected_response",
    [
        pytest.param(
            "user_info_with_many_tracking_points",
            {
                "tracking_labels": [
                    {"label": "Push ups", "description": "Description"},
                    {"label": "Running", "description": "Description"},
                ]
            },
            id="Tracking points labels available",
        ),
        pytest.param("basic_user_info", {"tracking_labels": []}, id="No Tracking points labels"),
    ],
    indirect=["user_info_fixture"],
)
def test_get_tracking_points_labels_success(
    user_info_fixture: UserInfo,
    expected_response: dict[str:Any],
    api_client_authenticated: APIClient,
):
    url = reverse(f"{app_name}:{GET_TRACKING_POINTS_LABELS_VIEW_NAME}")

    response: Response = api_client_authenticated.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


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
def test_get_tracking_points_labels_failed(
    client_fixture: APIClient,
    expected_status: status,
    expected_response: dict[str, Any],
):
    url = reverse(f"{app_name}:{GET_TRACKING_POINTS_LABELS_VIEW_NAME}")

    response: Response = client_fixture.get(url)

    assert response.status_code == expected_status
    assert response.json() == expected_response


@pytest.mark.django_db
class TestGetTrackingPointLabelsIncorrectHTTPMethods(GenericTestIncorrectHTTPMethods):
    VIEW_NAME = GET_TRACKING_POINTS_LABELS_VIEW_NAME
    ALLOWED_METHODS = ["get"]
