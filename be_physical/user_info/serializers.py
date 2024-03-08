from typing import Any, Iterable

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserInfo, UserTrackingLabel, UserTrackingPoint

GroupedTrackingPoint = tuple[str, Iterable[UserTrackingPoint]]


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = [
            "pk",
            "first_name",
            "last_name",
            "username",
            "email",
            "date_joined",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
        ]


class UserInfoSerializer(serializers.ModelSerializer[UserInfo]):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    date_joined = serializers.DateTimeField(source="user.date_joined")

    class Meta:
        model = UserInfo
        fields = ["username", "email", "height", "birth_date", "date_joined"]


class BiometricsSerializer(serializers.ModelSerializer[UserInfo]):
    weight = serializers.FloatField()
    desired_weight = serializers.SerializerMethodField()
    bmi_category = serializers.CharField()

    class Meta:
        model = UserInfo
        fields = ["height", "weight", "desired_weight", "bmi", "bmi_category"]

    def get_desired_weight(self, user_info: UserInfo) -> float | None:
        desired_weight_tracking_point = (
            user_info.tracking_points.filter(label__label="desired_weight").order_by("-date").first()
        )

        if desired_weight_tracking_point is not None:
            return desired_weight_tracking_point.value

        return None


class TrackingLabelSerializer(serializers.ModelSerializer[UserTrackingLabel]):
    class Meta:
        model = UserTrackingLabel
        fields = ["label", "description"]


class UserTrackingPointSerializer(serializers.ModelSerializer[UserTrackingPoint]):
    label = serializers.CharField()

    class Meta:
        model = UserTrackingPoint
        fields = ["label", "date", "value"]


class TrackingPointsSerializer(serializers.ModelSerializer[UserInfo]):
    tracking_points = UserTrackingPointSerializer(many=True)

    class Meta:
        model = UserInfo
        fields = ["tracking_points"]


class SimplifiedTrackingPointSerializer(serializers.ModelSerializer[UserTrackingPoint]):
    class Meta:
        model = UserTrackingPoint
        fields = ["date", "value"]


class GroupedTrackingPointSerializer(serializers.Serializer[GroupedTrackingPoint]):
    label = serializers.SerializerMethodField()
    values = serializers.SerializerMethodField()

    def get_label(self, data: GroupedTrackingPoint) -> str:
        return data[0]

    def get_values(self, data: GroupedTrackingPoint) -> dict[str, Any]:
        return SimplifiedTrackingPointSerializer(data[1], many=True).data


class GroupedTrackingPointsSerializer(serializers.Serializer[Iterable[GroupedTrackingPoint]]):
    tracking_points = serializers.SerializerMethodField()

    def get_tracking_points(self, data: Iterable[GroupedTrackingPoint]) -> dict[str, Any]:
        return GroupedTrackingPointSerializer(data, many=True).data


def serialize_grouped_tracking_groups(data: Iterable[GroupedTrackingPoint]) -> dict[str, Any]:
    serialized_data = {
        "tracking_points": [
            {
                "label": label,
                "values": [{"date": value.date, "value": value.value} for value in values],
            }
            for label, values in data
        ]
    }
    return serialized_data
