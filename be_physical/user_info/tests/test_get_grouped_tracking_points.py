import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from ..models import UserTrackingPoint
from ..serializers import GroupedTrackingPointsSerializer
from ..urls import GET_GROUPED_TRACKING_POINTS_VIEW_NAME, app_name
from ..views import LABELS_QUERY_PARAM


@pytest.mark.django_db
def test_get_grouped_tracking_points(
    user_tracking_point: UserTrackingPoint,
    api_client_authenticated: APIClient,
) -> None:
    input_data = [(user_tracking_point.label.label, [user_tracking_point])]  # Mimicking the itertools.groupby iterable
    expected_response = GroupedTrackingPointsSerializer(input_data).data

    url = reverse(f"{app_name}:{GET_GROUPED_TRACKING_POINTS_VIEW_NAME}")
    response: Response = api_client_authenticated.get(url, data={LABELS_QUERY_PARAM: "Push ups"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_grouped_tracking_points_no_auth(api_client: APIClient) -> None:
    expected_response = {"detail": "Authentication credentials were not provided."}

    url = reverse(f"{app_name}:{GET_GROUPED_TRACKING_POINTS_VIEW_NAME}")
    response: Response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_grouped_tracking_points_404(api_client_authenticated: APIClient) -> None:
    expected_response = {"detail": "Not found."}

    url = reverse(f"{app_name}:{GET_GROUPED_TRACKING_POINTS_VIEW_NAME}")
    response: Response = api_client_authenticated.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == expected_response
