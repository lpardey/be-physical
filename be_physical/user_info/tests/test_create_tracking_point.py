# import pytest
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.response import Response

# from ..models import UserInfo, UserTrackingLabel
# from ..urls import CREATE_TRACKING_POINT_VIEW_NAME, app_name
# from .conftest import APIClient, TrackingPointPayload


# @pytest.mark.django_db
# @pytest.mark.parametrize(
#     "test_payload, expected_status",
#     [
#         pytest.param(TrackingPointPayload(), status.HTTP_201_CREATED, id="Valid data"),
#         pytest.param(TrackingPointPayload(value=""), status.HTTP_400_BAD_REQUEST, id="Missing value field"),
#         pytest.param(
#             TrackingPointPayload(user_info_exists=False), status.HTTP_400_BAD_REQUEST, id="Invalid user info"
#         ),
#         pytest.param(TrackingPointPayload(label_exists=False), status.HTTP_400_BAD_REQUEST, id="Invalid label"),
#         pytest.param(TrackingPointPayload(date="invalid_date"), status.HTTP_400_BAD_REQUEST, id="Invalid date"),
#         pytest.param(TrackingPointPayload(value="invalid_value"), status.HTTP_400_BAD_REQUEST, id="Invalid value"),
#     ],
# )
# def test_create_tracking_point(
#     test_payload: TrackingPointPayload,
#     expected_status: status,
#     basic_user_info: UserInfo,
#     user_tracking_label: UserTrackingLabel,
#     api_client_authenticated: APIClient,
# ):
#     payload = test_payload.generate_payload(basic_user_info, user_tracking_label)

#     url = reverse(f"{app_name}:{CREATE_TRACKING_POINT_VIEW_NAME}")
#     response: Response = api_client_authenticated.post(url, payload)

#     assert response.status_code == expected_status

#     if expected_status == status.HTTP_201_CREATED:
#         expected_payload = dict(id=basic_user_info.user.pk, **payload)
#         expected_response = dict(data=expected_payload)
#         assert response.json() == expected_response


# @pytest.mark.django_db
# def test_create_tracking_point_no_auth(
#     basic_user_info: UserInfo,
#     user_tracking_label: UserTrackingLabel,
#     api_client: APIClient,
# ):
#     payload = TrackingPointPayload().generate_payload(basic_user_info, user_tracking_label)
#     expected_response = {"detail": "Authentication credentials were not provided."}

#     url = reverse(f"{app_name}:{CREATE_TRACKING_POINT_VIEW_NAME}")
#     response: Response = api_client.post(url, payload)

#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json() == expected_response
