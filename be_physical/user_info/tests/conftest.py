import datetime

import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ..models import UserInfo, UserTrackingPoint


@pytest.fixture
def user(db: None) -> User:
    user = User.objects.create(username="John", email="john@test.com", password="john1234")
    return user


@pytest.fixture
def user_info(user: User, db: None) -> UserInfo:
    birth_date = datetime.date.fromisoformat("1989-09-01")
    user_info = UserInfo.objects.create(user=user, height="1.86", birth_date=birth_date)
    return user_info


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user_token(db: None, user: User) -> str:
    token, _ = Token.objects.create(user=user)
    return str(token)


@pytest.fixture(scope="function")
def api_client_authenticated(api_client: APIClient, user: User) -> APIClient:
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def user_tracking_point(user_info: UserInfo, db: None) -> UserTrackingPoint:
    user_tracking_point = UserTrackingPoint.objects.create(user_info=user_info)
    return user_tracking_point
