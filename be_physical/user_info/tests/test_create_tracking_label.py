import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from ..models import UserTrackingLabel
from ..urls import CREATE_TRACKING_LABEL_VIEW_NAME, app_name
from .conftest import APIClient
from .payload import TrackingLabelPayload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_payload, expected_status",
    [
        pytest.param(TrackingLabelPayload(), status.HTTP_201_CREATED, id="Valid data"),
        pytest.param(TrackingLabelPayload(label=""), status.HTTP_400_BAD_REQUEST, id="Missing label field"),
        # pytest.param(TrackingLabelPayload(label=123), status.HTTP_400_BAD_REQUEST, id="Invalid data"),
        pytest.param(TrackingLabelPayload(label="duplicate"), status.HTTP_400_BAD_REQUEST, id="Duplicate label"),
    ],
)
def test_create_tracking_label(test_payload: TrackingLabelPayload, expected_status: status, api_client: APIClient):
    payload = test_payload.generate_payload()
    if payload["label"] == "duplicate":
        UserTrackingLabel.objects.create(label="duplicate", description="description")

    url = reverse(f"{app_name}:{CREATE_TRACKING_LABEL_VIEW_NAME}")
    response: Response = api_client.post(url, payload)

    assert response.status_code == expected_status

    if response.status_code == status.HTTP_201_CREATED:
        expected_response = dict(data=payload)
        assert response.json() == expected_response
