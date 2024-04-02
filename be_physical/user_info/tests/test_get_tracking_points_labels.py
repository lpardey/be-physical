from typing import Any

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from ..models import UserInfo
from ..urls import GET_TRACKING_POINTS_LABELS_VIEW_NAME, app_name


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_info, client_fixture, expected_status, expected_response",
    [
        pytest.param(
            "user_info_with_many_tracking_points",
            "api_client_authenticated",
            status.HTTP_200_OK,
            {
                "tracking_labels": [
                    {"label": "Push ups", "description": "Description"},
                    {"label": "Running", "description": "Description"},
                ]
            },
            id="Valid data",
        ),
        pytest.param(
            "user_info_with_many_tracking_points",
            "api_client",
            status.HTTP_401_UNAUTHORIZED,
            {"detail": "Authentication credentials were not provided."},
            id="No auth",
        ),
        pytest.param(
            "missing_user_info",
            "api_client_authenticated",
            status.HTTP_404_NOT_FOUND,
            {"detail": "No UserInfo matches the given query."},
            id="Missing UserInfo",
        ),
    ],
    indirect=["user_info", "client_fixture"],
)
def test_get_tracking_points_labels(
    user_info: UserInfo | None,
    client_fixture: APIClient,
    expected_status: status,
    expected_response: dict[str:Any],
):
    url = reverse(f"{app_name}:{GET_TRACKING_POINTS_LABELS_VIEW_NAME}")
    response: Response = client_fixture.get(url)

    assert response.status_code == expected_status
    assert response.json() == expected_response


# @pytest.mark.django_db
# def test_get_tracking_points_labels(
#     user_info_with_many_tracking_points: UserInfo,
#     api_client_authenticated: APIClient,
# ):
#     expected_response = {
#         "tracking_labels": [
#             {"label": "Push ups", "description": "Description"},
#             {"label": "Running", "description": "Description"},
#         ]
#     }
#     url = reverse(f"{app_name}:{GET_TRACKING_POINTS_LABELS_VIEW_NAME}")
#     response: Response = api_client_authenticated.get(url)

#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == expected_response


# @pytest.mark.django_db
# def test_get_tracking_points_labels_no_auth(api_client: APIClient):
#     expected_response = {"detail": "Authentication credentials were not provided."}

#     url = reverse(f"{app_name}:{GET_TRACKING_POINTS_LABELS_VIEW_NAME}")
#     response: Response = api_client.get(url)

#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json() == expected_response


# @pytest.mark.django_db
# def test_get_tracking_points_labels_missing_user_info(api_client_authenticated: APIClient):
#     expected_response = {"detail": "No UserInfo matches the given query."}

#     url = reverse(f"{app_name}:{GET_TRACKING_POINTS_LABELS_VIEW_NAME}")
#     response: Response = api_client_authenticated.get(url)

#     assert response.status_code == status.HTTP_404_NOT_FOUND
#     assert response.json() == expected_response
