import datetime

import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ..models import (
    AnnotationTypeChoices,
    ScopeChoices,
    StatusChoices,
    UserAnnotation,
    UserInfo,
    UserTrackingLabel,
    UserTrackingPoint,
)


@pytest.fixture
def user(db: None) -> User:
    user = User.objects.create(username="John", email="john@test.com", password="john1234")
    return user


@pytest.fixture(
    params=[
        pytest.param("basic_user_info", id="User without biometrics and annotations"),
        pytest.param("user_info_with_biometrics", id="User with biometrics"),
        pytest.param("user_info_with_annotations", id="User with annotations"),
        pytest.param("complete_user_info", id="User with biometrics and annotations"),
    ]
)
def user_info(request: pytest.FixtureRequest) -> UserInfo:
    fixture_value: UserInfo = request.getfixturevalue(request.param)
    return fixture_value


@pytest.fixture
def basic_user_info(user: User, db: None) -> UserInfo:
    user_info = UserInfo.objects.create(user=user, height="1.86", birth_date=datetime.date.fromisoformat("1989-09-01"))
    return user_info


@pytest.fixture
def user_info_with_biometrics(user: User, db: None) -> UserInfo:
    user_info = UserInfo.objects.create(user=user, height="1.86", birth_date=datetime.date.fromisoformat("1989-09-01"))
    weight_tracking_label = UserTrackingLabel.objects.create(label="weight", description="Measure in kgg")
    UserTrackingPoint.objects.create(
        user_info=user_info,
        label=weight_tracking_label,
        date=datetime.date.today(),
        value=90.0,
    )
    return user_info


@pytest.fixture
def user_info_with_annotations(user: User, db: None) -> UserInfo:
    user_info = UserInfo.objects.create(user=user, height="1.86", birth_date=datetime.date.fromisoformat("1989-09-01"))
    UserAnnotation.objects.create(
        user_info=user_info,
        text="I'm gonna run 10 miles today",
        annotation_type=AnnotationTypeChoices.GOAL,
        scope=ScopeChoices.USER,
        status=StatusChoices.ACTIVE,
    )
    return user_info


@pytest.fixture
def complete_user_info(user: User, db: None) -> UserInfo:
    user_info = UserInfo.objects.create(user=user, height="1.86", birth_date=datetime.date.fromisoformat("1989-09-01"))
    weight_tracking_label = UserTrackingLabel.objects.create(label="weight", description="Today's measure")
    UserTrackingPoint.objects.create(
        user_info=user_info,
        label=weight_tracking_label,
        date=datetime.date.today(),
        value=90.0,
    )
    desired_weight_label = UserTrackingLabel.objects.create(label="desired_weight", description="My goal weight")
    UserTrackingPoint.objects.create(
        user_info=user_info,
        label=desired_weight_label,
        date=datetime.date.today(),
        value=75.0,
    )
    UserAnnotation.objects.create(
        user_info=user_info,
        text="I'm gonna run 10 miles today",
        annotation_type=AnnotationTypeChoices.GOAL,
        scope=ScopeChoices.USER,
        status=StatusChoices.ACTIVE,
    )
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
