import datetime

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from ..models import UserInfo, UserTrackingLabel
from ..urls import CREATE_TRACKING_POINT_VIEW_NAME, app_name
from .conftest import APIClient


@pytest.mark.django_db
def test_create_tracking_point(
    basic_user_info: UserInfo,
    user_tracking_label: UserTrackingLabel,
    api_client_authenticated: APIClient,
):
    payload = {
        "user_info": basic_user_info.pk,
        "label": user_tracking_label.pk,
        "date": str(datetime.date.today()),
        "value": 10.0,
    }

    url = reverse(f"{app_name}:{CREATE_TRACKING_POINT_VIEW_NAME}")
    response: Response = api_client_authenticated.post(url, payload)

    assert response.status_code == status.HTTP_201_CREATED

    payload["id"] = basic_user_info.pk

    assert response.json() == payload
