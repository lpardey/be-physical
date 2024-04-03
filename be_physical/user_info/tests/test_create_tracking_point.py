import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from ..models import UserInfo, UserTrackingLabel, UserTrackingPoint
from ..urls import CREATE_TRACKING_POINT_VIEW_NAME, app_name
from .conftest import APIClient
from .generic_requests import TrackingPointRequest
from .generic_test_http_methods import GenericTestIncorrectHTTPMethods


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view_request, expected_status",
    [
        pytest.param(TrackingPointRequest(), status.HTTP_201_CREATED, id="Valid data"),
        pytest.param(TrackingPointRequest(value=""), status.HTTP_400_BAD_REQUEST, id="Missing value field"),
        pytest.param(
            TrackingPointRequest(user_info_exists=False), status.HTTP_400_BAD_REQUEST, id="Invalid user info"
        ),
        pytest.param(TrackingPointRequest(label_exists=False), status.HTTP_400_BAD_REQUEST, id="Invalid label"),
        pytest.param(TrackingPointRequest(date="invalid_date"), status.HTTP_400_BAD_REQUEST, id="Invalid date"),
        pytest.param(TrackingPointRequest(value="invalid_value"), status.HTTP_400_BAD_REQUEST, id="Invalid value"),
    ],
)
def test_create_tracking_point(
    view_request: TrackingPointRequest,
    expected_status: status,
    basic_user_info: UserInfo,
    user_tracking_label: UserTrackingLabel,
    api_client_authenticated: APIClient,
):
    request_data = view_request.generate_data(basic_user_info, user_tracking_label)
    url = reverse(f"{app_name}:{CREATE_TRACKING_POINT_VIEW_NAME}")

    response: Response = api_client_authenticated.post(url, request_data)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        expected_response = {"data": request_data}
        assert response.json() == expected_response
        assert UserTrackingPoint.objects.filter(user_info=basic_user_info)


@pytest.mark.django_db
def test_create_tracking_point_unauthorized(api_client: APIClient):
    url = reverse(f"{app_name}:{CREATE_TRACKING_POINT_VIEW_NAME}")

    response: Response = api_client.post(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestGetCreateTrackingPointIncorrectHTTPMethods(GenericTestIncorrectHTTPMethods):
    VIEW_NAME = CREATE_TRACKING_POINT_VIEW_NAME
    ALLOWED_METHODS = ["post"]
