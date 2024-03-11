import datetime

import pytest

from ..models import UserInfo, UserTrackingPoint
from ..serializers import (
    BiometricsSerializer,
    GroupedTrackingPointSerializer,
    SimplifiedTrackingPointSerializer,
    UserInfoSerializer,
)


@pytest.mark.django_db
def test_user_info_serializer(basic_user_info: UserInfo):
    data = UserInfoSerializer(basic_user_info).data
    data["date_joined"] = None  # Set to 'None' given its dynamic nature.
    expected_data = {
        "username": "John",
        "email": "john@test.com",
        "birth_date": str(datetime.date.fromisoformat("1989-09-01")),
        "date_joined": None,
    }

    assert data == expected_data


@pytest.mark.django_db
def test_biometrics_serializer(user_info_with_biometrics: UserInfo):
    data = BiometricsSerializer(user_info_with_biometrics).data
    expected_data = {
        "bmi": 26.01,
        "bmi_category": "overweight",
        "desired_weight": None,
        "height": "1.86",
        "weight": 90.0,
    }
    assert data == expected_data


@pytest.mark.django_db
def test_simplified_tracking_points_serializer(user_tracking_point: UserTrackingPoint):
    data = SimplifiedTrackingPointSerializer(user_tracking_point).data
    expected_data = {"date": str(datetime.date.today()), "value": 5.0}
    assert data == expected_data


@pytest.mark.django_db
def test_grouped_tracking_points_serializer(user_tracking_point: UserTrackingPoint):
    input_data = ("test_label", [user_tracking_point] * 2)
    data = GroupedTrackingPointSerializer(input_data).data
    expected_data = {"label": "test_label", "values": [{"date": str(datetime.date.today()), "value": 5.0}] * 2}
    assert data == expected_data
