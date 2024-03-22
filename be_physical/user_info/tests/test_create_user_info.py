import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from ..urls import CREATE_USER_INFO_VIEW_NAME, app_name
from .conftest import APIClient
from .payload import CreateUserInfoPayload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_payload, expected_status",
    [
        pytest.param(CreateUserInfoPayload(), status.HTTP_201_CREATED, id="Valid data"),
        pytest.param(CreateUserInfoPayload(user_exists=False), status.HTTP_400_BAD_REQUEST, id="Invalid user"),
        pytest.param(CreateUserInfoPayload(height=""), status.HTTP_400_BAD_REQUEST, id="Missing height field"),
        pytest.param(CreateUserInfoPayload(height="invalid_height"), status.HTTP_400_BAD_REQUEST, id="Invalid height"),
        pytest.param(CreateUserInfoPayload(birth_date="invalid_date"), status.HTTP_400_BAD_REQUEST, id="Invalid date"),
        pytest.param(CreateUserInfoPayload(birth_date=""), status.HTTP_400_BAD_REQUEST, id="Missing date field"),
    ],
)
def test_create_user_info(
    test_payload: CreateUserInfoPayload,
    expected_status: status,
    user: User,
    api_client_authenticated: APIClient,
):
    payload = test_payload.generate_payload(user)

    url = reverse(f"{app_name}:{CREATE_USER_INFO_VIEW_NAME}")
    response: Response = api_client_authenticated.post(url, payload)

    assert response.status_code == expected_status

    if response.status_code == status.HTTP_201_CREATED:
        expected_response = dict(data=payload)
        assert response.json() == expected_response


@pytest.mark.django_db
def test_create_user_info_no_auth(user: User, api_client: APIClient):
    payload = CreateUserInfoPayload().generate_payload(user)
    expected_response = {"detail": "Authentication credentials were not provided."}

    url = reverse(f"{app_name}:{CREATE_USER_INFO_VIEW_NAME}")
    response: Response = api_client.post(url, payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == expected_response
