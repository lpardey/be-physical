import datetime
from typing import Any
from unittest.mock import Mock, patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from ..models import UserInfo, UserTrackingLabel, UserTrackingPoint
from ..urls import GET_GROUPED_TRACKING_POINTS_VIEW_NAME, app_name

TEST_VALUE = 50


def generate_response(data: list[str] = ["push ups", "running", "squats"], value=TEST_VALUE) -> dict[str, Any]:
    parsed_data = [
        {
            "label": label,
            "values": [{"date": str(datetime.date.today()), "value": value}],
        }
        for label in data
    ]
    return dict(tracking_points=parsed_data)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "labels, expected_status, expected_response",
    [
        pytest.param(["push ups", "running", "squats"], status.HTTP_200_OK, generate_response(), id="With labels"),
        pytest.param([], status.HTTP_200_OK, generate_response(data=[]), id="Without labels"),
    ],
)
@patch("user_info.views.get_object_or_404")
@patch("user_info.views.serialize_grouped_tracking_groups")
def test_get_grouped_tracking_points(
    mock_serialize_grouped_tracking_groups: Mock,
    mock_get_object_or_404: Mock,
    labels: list[str],
    expected_status: status,
    expected_response: dict[str, Any],
    basic_user_info: UserInfo,
    api_client_authenticated: APIClient,
):
    mock_get_object_or_404.return_value = basic_user_info
    mock_serialize_grouped_tracking_groups.return_value = expected_response
    # Set up db
    for label in labels:
        tracking_label = UserTrackingLabel.objects.create(label=label, description=f"{label} description")
        UserTrackingPoint.objects.create(user_info=basic_user_info, label=tracking_label, value=TEST_VALUE)

    url = reverse(f"{app_name}:{GET_GROUPED_TRACKING_POINTS_VIEW_NAME}")
    response: Response = api_client_authenticated.get(url, data={"labels": labels})

    assert response.status_code == expected_status
    assert response.json() == expected_response
    assert mock_get_object_or_404.call_count == 1
    assert mock_serialize_grouped_tracking_groups.call_count == 1


@pytest.mark.django_db
def test_get_grouped_tracking_points_no_auth(api_client: APIClient):
    expected_response = {"detail": "Authentication credentials were not provided."}

    url = reverse(f"{app_name}:{GET_GROUPED_TRACKING_POINTS_VIEW_NAME}")
    response: Response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_grouped_tracking_points_404(api_client_authenticated: APIClient):
    expected_response = {"detail": "No UserInfo matches the given query."}

    url = reverse(f"{app_name}:{GET_GROUPED_TRACKING_POINTS_VIEW_NAME}")
    response: Response = api_client_authenticated.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == expected_response
