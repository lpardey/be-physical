import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


class GenericTestIncorrectHTTPMethods:
    VIEW_URL: str
    ALLOWED_METHODS: list[str] = ["get", "post", "put", "patch", "delete"]

    @pytest.mark.parametrize("http_method", ["get", "post", "put", "patch", "delete"])
    def test_incorrect_http_method(self, http_method: str, api_client_authenticated_with_user_info: APIClient):
        url = reverse(self.VIEW_URL)
        request_method = getattr(api_client_authenticated_with_user_info, http_method)

        response: Response = request_method(url)

        if http_method not in self.ALLOWED_METHODS:
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        else:
            assert response.status_code == status.HTTP_200_OK
