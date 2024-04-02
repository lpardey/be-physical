import datetime
from typing import Any
from unittest.mock import Mock, patch

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from ..models import UserInfo, UserTrackingLabel, UserTrackingPoint
from ..serializers import GroupedTrackingPointsQueryParamsSerializer
from ..urls import GET_GROUPED_TRACKING_POINTS_VIEW_NAME, app_name
from .conftest import PERMISSION_DENIED_RESPONSE, UNAUTHORIZED_RESPONSE, USER_INFO_NOT_FOUND_RESPONSE

LABEL_TEST_VALUE = 50.0


def generate_response(data: list[str], value: Any) -> dict[str, Any]:
    response = {
        "tracking_points": [
            {
                "label": label,
                "values": [{"date": str(datetime.date.today()), "value": value}],
            }
            for label in data
        ]
    }
    return response


def set_up_labels_in_db(user_info: UserInfo, labels: list[str], label_value: Any) -> None:
    for label in labels:
        tracking_label = UserTrackingLabel.objects.create(label=label, description=f"{label} description")
        UserTrackingPoint.objects.create(user_info=user_info, label=tracking_label, value=label_value)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "labels, expected_status",
    [
        pytest.param("jumping,running,swimming", status.HTTP_200_OK, id="Valid request"),
        pytest.param("", status.HTTP_400_BAD_REQUEST, id="Empty request"),
        pytest.param(",", status.HTTP_400_BAD_REQUEST, id="Request with comma only"),
        pytest.param([], status.HTTP_400_BAD_REQUEST, id="Empty request (list)"),
    ],
)
@patch("user_info.views.get_object_or_404")
def test_get_grouped_tracking_points(
    m_get_object_or_404: Mock,
    labels: str,
    expected_status: status,
    basic_user_info: UserInfo,
    api_client_authenticated: APIClient,
):
    m_get_object_or_404.return_value = basic_user_info
    request_data = {"labels": labels}
    url = reverse(f"{app_name}:{GET_GROUPED_TRACKING_POINTS_VIEW_NAME}")
    if expected_status == status.HTTP_200_OK:
        deserialized_labels = GroupedTrackingPointsQueryParamsSerializer().validate_labels(labels)
        set_up_labels_in_db(basic_user_info, deserialized_labels, LABEL_TEST_VALUE)

    response: Response = api_client_authenticated.get(url, request_data)

    assert response.status_code == expected_status
    assert m_get_object_or_404.call_count == 1
    if expected_status == status.HTTP_200_OK:
        assert response.json() == generate_response(deserialized_labels, LABEL_TEST_VALUE)


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
def test_get_grouped_tracking_points_failed(
    client_fixture: APIClient,
    expected_status: status,
    expected_response: dict[str, Any],
):
    url = reverse(f"{app_name}:{GET_GROUPED_TRACKING_POINTS_VIEW_NAME}")

    response: Response = client_fixture.get(url)

    assert response.status_code == expected_status
    assert response.json() == expected_response


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_fixture, expected_status",
    [
        pytest.param("user", status.HTTP_403_FORBIDDEN),
        pytest.param("admin_user", status.HTTP_200_OK),
        pytest.param("superuser", status.HTTP_200_OK),
    ],
    indirect=["user_fixture"],
)
@patch("user_info.views.get_object_or_404")
@patch("user_info.views.serialize_grouped_tracking_groups")
def test_get_grouped_tracking_points_permission_denied(
    m_serialize_grouped_tracking_groups: Mock,
    m_get_object_or_404: Mock,
    user_fixture: User,
    expected_status: status,
    other_user_info: UserInfo,
    api_client_authenticated: APIClient,
):
    m_get_object_or_404.return_value = other_user_info
    request_data = {"labels": "push ups,running,squats"}
    labels = GroupedTrackingPointsQueryParamsSerializer().validate_labels(request_data["labels"])
    m_serialize_grouped_tracking_groups.return_value = generate_response(labels, LABEL_TEST_VALUE)
    url = reverse(f"{app_name}:{GET_GROUPED_TRACKING_POINTS_VIEW_NAME}")
    expected_response = (
        PERMISSION_DENIED_RESPONSE
        if expected_status == status.HTTP_403_FORBIDDEN
        else m_serialize_grouped_tracking_groups.return_value
    )

    response: Response = api_client_authenticated.get(url, request_data)

    assert response.status_code == expected_status
    assert response.json() == expected_response


@pytest.mark.django_db
@pytest.mark.parametrize("http_method", ["post", "put", "patch", "delete"])
def test_get_grouped_tracking_points_incorrect_http_method(http_method: str, api_client_authenticated: APIClient):
    url = reverse(f"{app_name}:{GET_GROUPED_TRACKING_POINTS_VIEW_NAME}")
    request_method = getattr(api_client_authenticated, http_method)

    response: Response = request_method(url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
