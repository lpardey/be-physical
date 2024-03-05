import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from ..models import UserInfo
from ..serializers import UserInfoSerializer
from ..urls import GET_DATA_VIEW_NAME, app_name


@pytest.mark.django_db
def test_get_data(basic_user_info: UserInfo, api_client_authenticated: APIClient) -> None:
    expected_response = UserInfoSerializer(basic_user_info).data

    url = reverse(f"{app_name}:{GET_DATA_VIEW_NAME}")
    response: Response = api_client_authenticated.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_data_no_auth(api_client: APIClient) -> None:
    expected_response = {"detail": "Authentication credentials were not provided."}

    url = reverse(f"{app_name}:{GET_DATA_VIEW_NAME}")
    response: Response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == expected_response