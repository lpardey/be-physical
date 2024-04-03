import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from ..urls import app_name

ALL_METHODS = ["get", "post", "put", "patch", "delete"]


class GenericTestIncorrectHTTPMethods:
    VIEW_NAME: str
    ALLOWED_METHODS: list[str] = ALL_METHODS

    @pytest.mark.parametrize("http_method", ALL_METHODS)
    def test_incorrect_http_method(self, http_method: str, api_client_authenticated_with_user_info: APIClient):
        url = reverse(f"{app_name}:{self.VIEW_NAME}")
        request_method = getattr(api_client_authenticated_with_user_info, http_method)

        response: Response = request_method(url)

        if http_method not in self.ALLOWED_METHODS:
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        else:
            pytest.skip(f"Skipping test for allowed methods: {self.ALLOWED_METHODS}")
