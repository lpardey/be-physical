from typing import Any, Iterable

# from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from rest_framework import serializers

from .models import UserAnnotation, UserInfo, UserTrackingLabel, UserTrackingPoint

GroupedTrackingPoint = tuple[str, Iterable[UserTrackingPoint]]


class UserInfoSerializer(serializers.ModelSerializer[UserInfo]):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    date_joined = serializers.DateTimeField(source="user.date_joined")

    class Meta:
        model = UserInfo
        fields = ["username", "email", "birth_date", "date_joined"]


class CreateUserInfoRequestSerializer(serializers.ModelSerializer[UserInfo]):
    class Meta:
        model = UserInfo
        fields = "__all__"


# class UserSerializer(serializers.ModelSerializer[User]):
#     user_info = CreateUserInfoRequestSerializer()

#     class Meta:
#         model = User
#         fields = ["username", "password", "email", "user_info"]
#         extra_kwargs = {"password": {"write_only": True}}

#     def create(self, validated_data: dict[str, Any]) -> User:
#         user_info_data = validated_data.pop("user_info")
#         password = validated_data.pop("password")
#         user, created = User.objects.get_or_create(**validated_data)
#         user.set_password(password)
#         user.save()
#         UserInfo.objects.create(user=user, **user_info_data)
#         return user


class BiometricsSerializer(serializers.ModelSerializer[UserInfo]):
    desired_weight = serializers.SerializerMethodField(method_name="get_desired_weight")

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
        fields = "__all__"  # All fields in the model should be used


def serialize_tracking_points_labels(data: QuerySet | list[UserTrackingLabel]) -> dict[str, Any]:
    serialized_data = {"tracking_labels": [{label.label: label.description} for label in data]}
    return serialized_data


class UserTrackingPointSerializer(serializers.ModelSerializer[UserTrackingPoint]):
    class Meta:
        model = UserTrackingPoint
        fields = ["label", "date", "value"]


class TrackingPointsSerializer(serializers.ModelSerializer[UserInfo]):
    tracking_points = UserTrackingPointSerializer(many=True)

    class Meta:
        model = UserInfo
        fields = ["tracking_points"]


class TrackingPointRequestSerializer(serializers.ModelSerializer[UserTrackingPoint]):
    class Meta:
        model = UserTrackingPoint
        fields = "__all__"


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


class UserAnnotationSerializer(serializers.ModelSerializer[UserAnnotation]):
    class Meta:
        model = UserAnnotation
        fields = ["text", "annotation_type", "scope", "status"]


class AnnotationsSerializer(serializers.ModelSerializer[UserInfo]):
    annotations = UserAnnotationSerializer(many=True)

    class Meta:
        model = UserInfo
        fields = ["annotations"]


class AnnotationRequestSerializer(serializers.ModelSerializer[UserAnnotation]):
    class Meta:
        model = UserAnnotation
        fields = "__all__"
