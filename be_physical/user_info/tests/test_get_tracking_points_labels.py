from unittest.mock import Mock, patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from ..models import UserInfo
from ..urls import GET_TRACKING_POINTS_LABELS_VIEW_NAME, app_name


@pytest.mark.django_db
@patch("user_info.views.get_object_or_404")
@patch("user_info.views.serialize_tracking_points_labels")
def test_get_tracking_points_labels(
    mock_serialize_tracking_points_labels: Mock,
    mock_get_object_or_404: Mock,
    basic_user_info: UserInfo,
    api_client_authenticated: APIClient,
):
    mock_get_object_or_404.return_value = basic_user_info
    mock_serialize_tracking_points_labels.return_value = {
        "tracking_points_labels": [
            {"label_1": "description_1"},
            {"label_2": "description_2"},
            {"label_3": "description_3"},
        ]
    }
    expected_response = mock_serialize_tracking_points_labels.return_value

    url = reverse(f"{app_name}:{GET_TRACKING_POINTS_LABELS_VIEW_NAME}")
    response: Response = api_client_authenticated.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_tracking_points_labels_no_auth(api_client: APIClient):
    expected_response = {"detail": "Authentication credentials were not provided."}

    url = reverse(f"{app_name}:{GET_TRACKING_POINTS_LABELS_VIEW_NAME}")
    response: Response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_tracking_points_labels_404(api_client_authenticated: APIClient):
    expected_response = {"detail": "Not found."}

    url = reverse(f"{app_name}:{GET_TRACKING_POINTS_LABELS_VIEW_NAME}")
    response: Response = api_client_authenticated.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == expected_response
