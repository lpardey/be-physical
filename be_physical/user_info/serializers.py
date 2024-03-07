from django.contrib.auth.models import User
from rest_framework import serializers

from .models import AnnotationTypeChoices, ScopeChoices, StatusChoices, UserInfo, UserTrackingLabel, UserTrackingPoint


class UserSerializer(serializers.ModelSerializer):
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


class UserInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    date_joined = serializers.DateTimeField(source="user.date_joined")

    class Meta:
        model = UserInfo
        fields = ["username", "email", "height", "birth_date", "date_joined"]


class BiometricsSerializer(serializers.ModelSerializer):
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


class TrackingLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTrackingLabel
        fields = ["label", "description"]


class UserTrackingPointSerializer(serializers.ModelSerializer):
    label = serializers.CharField()

    class Meta:
        model = UserTrackingPoint
        fields = ["label", "date", "value"]


class TrackingPointsSerializer(serializers.ModelSerializer):
    tracking_points = UserTrackingPointSerializer(many=True)

    class Meta:
        model = UserInfo
        fields = ["tracking_points"]
