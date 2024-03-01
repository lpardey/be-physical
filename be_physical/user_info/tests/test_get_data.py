import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from ..models import UserInfo
from ..urls import GET_DATA_VIEW_NAME, app_name


@pytest.mark.django_db
def test_get_data(user_info: UserInfo, api_client_authenticated: APIClient) -> None:
    expected_response = {
        "username": user_info.user.username,
        "email": user_info.user.email,
        "height": user_info.height,
        "birth_date": user_info.birth_date.isoformat(),
        "date_joined": user_info.user.date_joined.replace(tzinfo=None).isoformat() + "Z",
    }

    url = reverse(f"{app_name}:{GET_DATA_VIEW_NAME}")
    response: Response = api_client_authenticated.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_data_no_auth(user_info: UserInfo, api_client: APIClient) -> None:
    expected_response = {"detail": "Authentication credentials were not provided."}

    url = reverse(f"{app_name}:{GET_DATA_VIEW_NAME}")
    response: Response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == expected_response
