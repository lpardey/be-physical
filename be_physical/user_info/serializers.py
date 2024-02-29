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
    weight = serializers.SerializerMethodField()
    desired_weight = serializers.SerializerMethodField()
    bmi_category = serializers.CharField(source="category_name_by_bmi")

    class Meta:
        model = UserInfo
        fields = ["height", "weight", "desired_weight", "bmi", "bmi_category"]

    def get_weight(self, user_info: UserInfo):
        latest_weight_filter = user_info.tracking_points.filter(label__label="weight").order_by("-date")
        latest_weight_record = latest_weight_filter.values_list("value", flat=True).first()
        return latest_weight_record

    def get_desired_weight(self, user_info: UserInfo):
        desired_weight_filter = user_info.tracking_points.filter(label__label="desired_weight").order_by("-date")
        desired_weight_record = desired_weight_filter.values_list("value", flat=True).first()
        return desired_weight_record


class TrackingLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTrackingLabel
        fields = ["label", "description"]


class UerTrackingPointSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="label.label")
    description = serializers.CharField(source="label.description")

    class Meta:
        model = UserTrackingPoint
        fields = ["label", "description", "date", "value"]


class TrackingPointsSerializer(serializers.ModelSerializer):
    tracking_points = UerTrackingPointSerializer(many=True)

    class Meta:
        model = UserInfo
        fields = ["tracking_points"]


class AnnotationSerializer(serializers.Serializer):
    text = serializers.CharField()
    annotation_type = serializers.ChoiceField(choices=AnnotationTypeChoices.choices)
    scope = serializers.ChoiceField(choices=ScopeChoices.choices)
    status = serializers.ChoiceField(choices=StatusChoices.choices)


class AnnotationsData(serializers.Serializer):
    annotations = list[AnnotationSerializer] | None
