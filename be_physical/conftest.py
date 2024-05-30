import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotAuthenticated
from rest_framework.test import APIClient
from user_info.models import UserInfo


@pytest.fixture
def user(db: None) -> User:
    user = User.objects.create_user(username="John", email="john@test.com", password="john1234")
    return user


@pytest.fixture
def user_token(db: None, user: User) -> str:
    token, _ = Token.objects.create(user=user)
    return str(token)


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture()
def api_client_authenticated(api_client: APIClient, user: User) -> APIClient:
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture(
    params=[
        pytest.param("api_client", id="Basic client (not authenticated)"),
        pytest.param("api_client_authenticated", id="Basic client (authenticated)"),
    ]
)
def client_fixture(request: pytest.FixtureRequest) -> UserInfo:
    fixture_value: UserInfo = request.getfixturevalue(request.param)
    return fixture_value


@pytest.fixture
def unauthorized_response() -> dict[str, str]:
    return {"detail": NotAuthenticated.default_detail}


@pytest.fixture
def user_info_not_found_response() -> dict[str, str]:
    return {"detail": "No UserInfo matches the given query."}


@pytest.fixture(
    params=[
        pytest.param("unauthorized_response", id="Unauthorized"),
        pytest.param("user_info_not_found_response", id="UserInfo not found"),
    ]
)
def expected_response_fixture(request: pytest.FixtureRequest) -> dict[str, str]:
    fixture_value = request.getfixturevalue(request.param)
    return fixture_value
