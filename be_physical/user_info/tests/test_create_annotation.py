import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from ..models import UserInfo
from ..urls import CREATE_ANNOTATION_VIEW_NAME, app_name
from .conftest import AnnotationPayload, APIClient


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_payload, expected_status",
    [
        pytest.param(AnnotationPayload(), status.HTTP_201_CREATED, id="Valid data"),
        pytest.param(AnnotationPayload(text=""), status.HTTP_400_BAD_REQUEST, id="Missing text field"),
        pytest.param(AnnotationPayload(user_info_exists=False), status.HTTP_400_BAD_REQUEST, id="Invalid user info"),
        pytest.param(
            AnnotationPayload(annotation_type="invalid_annotation_type"),
            status.HTTP_400_BAD_REQUEST,
            id="Invalid annotation type",
        ),
        pytest.param(AnnotationPayload(scope="invalid_scope"), status.HTTP_400_BAD_REQUEST, id="Invalid scope"),
        pytest.param(AnnotationPayload(status="invalid_status"), status.HTTP_400_BAD_REQUEST, id="Invalid status"),
    ],
)
def test_create_annotation(
    test_payload: AnnotationPayload,
    expected_status: status,
    basic_user_info: UserInfo,
    api_client_authenticated: APIClient,
):
    payload = test_payload.generate_payload(basic_user_info)

    url = reverse(f"{app_name}:{CREATE_ANNOTATION_VIEW_NAME}")
    response: Response = api_client_authenticated.post(url, payload)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        expected_payload = dict(id=basic_user_info.user.pk, **payload)
        expected_response = dict(data=expected_payload)
        assert response.json() == expected_response


@pytest.mark.django_db
def test_create_annotation_no_auth(basic_user_info: UserInfo, api_client: APIClient):
    payload = AnnotationPayload().generate_payload(basic_user_info)
    expected_response = {"detail": "Authentication credentials were not provided."}

    url = reverse(f"{app_name}:{CREATE_ANNOTATION_VIEW_NAME}")
    response: Response = api_client.post(url, payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == expected_response
