import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from ..models import UserInfo
from ..serializers import AnnotationsSerializer
from ..urls import GET_ANNOTATIONS_VIEW_NAME, app_name


@pytest.mark.django_db
def test_get_annotations(user_info: UserInfo, api_client_authenticated: APIClient):
    expected_response = AnnotationsSerializer(user_info).data
    url = reverse(f"{app_name}:{GET_ANNOTATIONS_VIEW_NAME}")
    response: Response = api_client_authenticated.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_annotations_no_auth(api_client: APIClient):
    expected_response = {"detail": "Authentication credentials were not provided."}

    url = reverse(f"{app_name}:{GET_ANNOTATIONS_VIEW_NAME}")
    response: Response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_annotations_404(api_client_authenticated: APIClient):
    expected_response = {"detail": "No UserInfo matches the given query."}

    url = reverse(f"{app_name}:{GET_ANNOTATIONS_VIEW_NAME}")
    response: Response = api_client_authenticated.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == expected_response
