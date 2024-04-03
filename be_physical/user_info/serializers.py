from typing import Any, Iterable

from django.utils.translation import gettext as _
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

    def validate_label(self, value: str) -> str:
        # Label already exists
        if UserTrackingLabel.objects.filter(label=value).exists():
            raise serializers.ValidationError("Label already exists.")

        return value


def serialize_tracking_points_labels(data: Iterable[UserTrackingLabel]) -> dict[str, Any]:
    values = (TrackingLabelSerializer(label).data for label in data)
    serialized_data = {"tracking_labels": sorted(values, key=lambda x: x["label"])}
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


class GroupedTrackingPointsQueryParamsSerializer(serializers.Serializer[serializers.CharField]):
    labels = serializers.CharField(
        required=True,
        help_text=_("Comma-separated list of labels"),
    )

    def validate_labels(self, value: str) -> list[str]:
        labels = [label for label in value.split(",") if label]

        if not labels:
            detail = _("At least one label must be provided.")
            raise serializers.ValidationError(detail)

        return labels


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
