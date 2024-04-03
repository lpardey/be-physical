import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from ..models import UserAnnotation, UserInfo
from ..urls import CREATE_ANNOTATION_VIEW_NAME, app_name
from .conftest import APIClient
from .generic_requests import AnnotationRequest
from .generic_test_http_methods import GenericTestIncorrectHTTPMethods


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view_request, expected_status",
    [
        pytest.param(AnnotationRequest(), status.HTTP_201_CREATED, id="Valid data"),
        pytest.param(AnnotationRequest(text=""), status.HTTP_400_BAD_REQUEST, id="Missing text field"),
        pytest.param(AnnotationRequest(user_info_exists=False), status.HTTP_400_BAD_REQUEST, id="Invalid user info"),
        pytest.param(
            AnnotationRequest(annotation_type="invalid_annotation_type"),
            status.HTTP_400_BAD_REQUEST,
            id="Invalid annotation type",
        ),
        pytest.param(AnnotationRequest(scope="invalid_scope"), status.HTTP_400_BAD_REQUEST, id="Invalid scope"),
        pytest.param(AnnotationRequest(status="invalid_status"), status.HTTP_400_BAD_REQUEST, id="Invalid status"),
    ],
)
def test_create_annotation(
    view_request: AnnotationRequest,
    expected_status: status,
    basic_user_info: UserInfo,
    api_client_authenticated: APIClient,
):
    request_data = view_request.generate_data(basic_user_info)
    url = reverse(f"{app_name}:{CREATE_ANNOTATION_VIEW_NAME}")

    response: Response = api_client_authenticated.post(url, request_data)

    assert response.status_code == expected_status
    if expected_status == status.HTTP_201_CREATED:
        expected_response = {"data": request_data}
        assert response.json() == expected_response
        assert UserAnnotation.objects.filter(user_info=basic_user_info)


@pytest.mark.django_db
def test_create_annotation_unauthorized(api_client: APIClient):
    url = reverse(f"{app_name}:{CREATE_ANNOTATION_VIEW_NAME}")

    response: Response = api_client.post(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestGetCreateAnnotationIncorrectHTTPMethods(GenericTestIncorrectHTTPMethods):
    VIEW_NAME = CREATE_ANNOTATION_VIEW_NAME
    ALLOWED_METHODS = ["post"]
