import datetime

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from ..urls import CREATE_USER_INFO_VIEW_NAME, app_name
from .conftest import APIClient


@pytest.mark.django_db
@pytest.mark.parametrize(
    "users, height, birth_date, client, expected_status",
    [
        pytest.param(
            "user",
            "2.00",
            "1989-09-01",
            "api_client_authenticated",
            status.HTTP_201_CREATED,
            id="Valid request as regular user",
        ),
        pytest.param(
            "admin_user",
            "2.00",
            "1989-09-01",
            "api_client_authenticated",
            status.HTTP_201_CREATED,
            id="Valid request as admin user",
        ),
        pytest.param(
            "superuser",
            "2.00",
            "1989-09-01",
            "api_client_authenticated",
            status.HTTP_201_CREATED,
            id="Valid request as superuser",
        ),
        pytest.param(
            "user",
            "invalid_height",
            "1989-09-01",
            "api_client_authenticated",
            status.HTTP_400_BAD_REQUEST,
            id="Invalid height",
        ),
        pytest.param(
            "user",
            "5.4563",
            "1989-09-01",
            "api_client_authenticated",
            status.HTTP_400_BAD_REQUEST,
            id="Height with more than two decimal values",
        ),
        pytest.param(
            "user",
            "5.00",
            "1989-09-01",
            "api_client_authenticated",
            status.HTTP_400_BAD_REQUEST,
            id="Height value out of upper bound",
        ),
        pytest.param(
            "user",
            "0.99",
            "1989-09-01",
            "api_client_authenticated",
            status.HTTP_400_BAD_REQUEST,
            id="Height value out of lower bound",
        ),
        pytest.param(
            "user",
            "",
            "1989-09-01",
            "api_client_authenticated",
            status.HTTP_400_BAD_REQUEST,
            id="Missing height",
        ),
        pytest.param(
            "user",
            "2.00",
            "invalid_date",
            "api_client_authenticated",
            status.HTTP_400_BAD_REQUEST,
            id="Invalid date",
        ),
        pytest.param(
            "user",
            "2.00",
            datetime.date.today() + datetime.timedelta(days=1),
            "api_client_authenticated",
            status.HTTP_400_BAD_REQUEST,
            id="Birth date out of upper bound",
        ),
        pytest.param(
            "user",
            "2.00",
            "1899-01-01",
            "api_client_authenticated",
            status.HTTP_400_BAD_REQUEST,
            id="Birth date out of lower bound",
        ),
        pytest.param(
            "user",
            "2.00",
            "",
            "api_client_authenticated",
            status.HTTP_400_BAD_REQUEST,
            id="Missing date",
        ),
        pytest.param(
            "user",
            "2.00",
            "1989-09-01",
            "api_client",
            status.HTTP_401_UNAUTHORIZED,
            id="Unauthorized user",
        ),
    ],
    indirect=["users", "client"],
)
def test_create_user_info(users: User, height: float, birth_date: str, client: APIClient, expected_status: status):
    data = {"user": users.pk, "height": height, "birth_date": birth_date}

    url = reverse(f"{app_name}:{CREATE_USER_INFO_VIEW_NAME}")
    response: Response = client.post(url, data)

    assert response.status_code == expected_status

    if response.status_code == status.HTTP_201_CREATED:
        expected_response = dict(data=data)
        assert response.json() == expected_response
