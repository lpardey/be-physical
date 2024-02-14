import math
from enum import Enum, IntEnum, StrEnum, auto

from django.contrib.auth.models import User
from django.db import models

from ..be_physical.common import get_choices

# Create your models here.


class UserInfo(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    height = models.DecimalField(max_digits=3, decimal_places=2, blank=False, null=False, help_text="Height in meters")
    birth_date = models.DateField(blank=False, null=False, help_text="Birthdate as day/month/year")
    annotations: models.QuerySet["UserAnnotation"]
    tracking_points: models.QuerySet["UserTrackingPoint"]

    @property
    def bmi(self) -> float | None:
        latest_weight = self.tracking_points.filter(label__eq="weight").order_by("-date").first()

        if latest_weight is not None:
            return latest_weight / (self.height**2)

        return None

    @property
    def category_by_bmi(self) -> str | None:
        if self.bmi is None:
            return None

        for category in BMICategory:
            if category.lower_bound <= self.bmi <= category.upper_bound:
                return category.label.replace("_", " ").title()


class BMICategory(Enum):
    UNDERWEIGHT = (0, 18.4, auto())
    HEALTHY_WEIGHT = (18.5, 24.9, auto())
    OVERWEIGHT = (25.0, 29.9, auto())
    OBESITY_CLASS_I = (30.0, 34.9, auto())
    OBESITY_CLASS_II = (35.0, 39.9, auto())
    OBESITY_CLASS_III = (40.0, math.inf, auto())

    @property
    def lower_bound(self) -> float:
        return self.value[0]

    @property
    def upper_bound(self) -> float:
        return self.value[1]

    @property
    def label(self) -> str:
        return self.value[2]


class StatusEnum(IntEnum):
    INACTIVE = 0
    ACTIVE = auto()


class AnnotationScopeEnum(StrEnum):
    USER = auto()
    TRAINER = auto()


class AnnotationTypeEnum(StrEnum):
    GENERAL = auto()
    GOAL = auto()
    RESTRICTION = auto()
    TRAINER_ANNOTATION = auto()


ANNOTATION_TYPE_CHOICES = get_choices(AnnotationTypeEnum, str)
SCOPE_CHOICES = get_choices(AnnotationScopeEnum, str)
STATUS_CHOICES = get_choices(StatusEnum, int)


class UserAnnotation(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="annotations")
    text = models.TextField(max_length=500)
    annotation_type = models.CharField(max_length=64, choices=ANNOTATION_TYPE_CHOICES)
    scope = models.CharField(max_length=64, choices=SCOPE_CHOICES)
    status = models.IntegerField(choices=STATUS_CHOICES)


class UserTrackingPoint(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE, db_index=True, related_name="tracking_points")
    label = models.CharField(max_length=64, blank=False, db_index=True)
    date = models.DateField(blank=False, null=False, auto_now=True)
    value = models.FloatField()
