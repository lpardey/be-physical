import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from ..models import UserTrackingLabel
from ..urls import CREATE_TRACKING_LABEL_VIEW_NAME, app_name
from .conftest import APIClient
from .generic_requests import TrackingLabelRequest
from .generic_test_http_methods import GenericTestIncorrectHTTPMethods


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view_request, expected_status",
    [
        pytest.param(TrackingLabelRequest(), status.HTTP_201_CREATED, id="Valid data"),
        pytest.param(TrackingLabelRequest(label=""), status.HTTP_400_BAD_REQUEST, id="Missing label field"),
        pytest.param(TrackingLabelRequest(label="duplicate"), status.HTTP_400_BAD_REQUEST, id="Duplicate label"),
    ],
)
def test_create_tracking_label(
    view_request: TrackingLabelRequest,
    expected_status: status,
    api_client_authenticated: APIClient,
):
    request_data = view_request.generate_data()
    url = reverse(f"{app_name}:{CREATE_TRACKING_LABEL_VIEW_NAME}")
    if request_data["label"] == "duplicate":
        UserTrackingLabel.objects.create(label="duplicate", description="description")

    response: Response = api_client_authenticated.post(url, request_data)

    assert response.status_code == expected_status
    if response.status_code == status.HTTP_201_CREATED:
        expected_response = {"data": request_data}
        assert response.json() == expected_response
        assert UserTrackingLabel.objects.filter(label=request_data["label"]).count() == 1


@pytest.mark.django_db
def test_create_tracking_label_unauthorized(api_client: APIClient):
    url = reverse(f"{app_name}:{CREATE_TRACKING_LABEL_VIEW_NAME}")

    response: Response = api_client.post(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestGetCreateTrackingLabelIncorrectHTTPMethods(GenericTestIncorrectHTTPMethods):
    VIEW_NAME = CREATE_TRACKING_LABEL_VIEW_NAME
    ALLOWED_METHODS = ["post"]
