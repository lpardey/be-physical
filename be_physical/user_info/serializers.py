from django.contrib.auth.models import User
from rest_framework import serializers

from .models import AnnotationTypeChoices, ScopeChoices, StatusChoices, UserInfo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
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
        )


class UserInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    date_joined = serializers.DateTimeField(source="user.date_joined")

    class Meta:
        model = UserInfo
        fields = ("username", "email", "height", "birth_date", "date_joined")


class BiometricsSerializer(serializers.Serializer):
    height = serializers.DecimalField(max_digits=3, decimal_places=2, min_value=1.0, max_value=2.5)
    weight = serializers.FloatField(allow_null=True)
    desired_weight = serializers.FloatField(allow_null=True)
    bmi = serializers.FloatField(allow_null=True)
    bmi_category = serializers.CharField(allow_null=True)


class TrackingPointSerializer(serializers.Serializer):
    label = serializers.CharField()
    description = serializers.CharField()
    date = serializers.DateField()
    value = serializers.FloatField(allow_null=True, min_value=0)


class TrackingPointsData(serializers.Serializer):
    tracking_points = list[TrackingPointSerializer] | None


class AnnotationSerializer(serializers.Serializer):
    text = serializers.CharField()
    annotation_type = serializers.ChoiceField(choices=AnnotationTypeChoices.choices)
    scope = serializers.ChoiceField(choices=ScopeChoices.choices)
    status = serializers.ChoiceField(choices=StatusChoices.choices)


class AnnotationsData(serializers.Serializer):
    annotations = list[AnnotationSerializer] | None
