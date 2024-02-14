import math
from enum import Enum

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class UserInfo(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    height = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=False,
        null=False,
        help_text=_("Height in meters"),
        validators=[MinValueValidator(1.0), MaxValueValidator(2.5)],
    )
    birth_date = models.DateField(blank=False, null=False, help_text=_("Birthdate as day/month/year"))
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
                return category.label

    def __str__(self) -> str:
        return _(f"User #{self.user_id} information")


class BMICategory(Enum):
    """
    Based on the World Health Organization (WHO) guidelines
    """

    UNDERWEIGHT = (0, 18.4)
    HEALTHY_WEIGHT = (18.5, 24.9)
    OVERWEIGHT = (25.0, 29.9)
    OBESITY_CLASS_I = (30.0, 34.9)
    OBESITY_CLASS_II = (35.0, 39.9)
    OBESITY_CLASS_III = (40.0, math.inf)

    @property
    def lower_bound(self) -> float:
        return self.value[0]

    @property
    def upper_bound(self) -> float:
        return self.value[1]

    @property
    def label(self) -> str:
        return _(self.name.replace("_", " ").title())


class StatusChoices(models.IntegerChoices):
    INACTIVE = 0, _("Inactive")
    ACTIVE = 1, _("Active")


class ScopeChoices(models.TextChoices):
    USER = _("User")
    TRAINER = _("Trainer")


class AnnotationTypeChoices(models.TextChoices):
    GENERAL = _("General")
    GOAL = _("Goal")
    RESTRICTION = _("Restriction")
    TRAINER_ANNOTATION = _("Trainer Annotation")


class UserAnnotation(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="annotations")
    text = models.TextField(max_length=500)
    annotation_type = models.CharField(
        max_length=64, choices=AnnotationTypeChoices, default=AnnotationTypeChoices.GENERAL
    )
    scope = models.CharField(max_length=64, choices=ScopeChoices, default=ScopeChoices.USER)
    status = models.IntegerField(choices=StatusChoices, blank=True, null=True, default=StatusChoices.ACTIVE)


class UserTrackingPoint(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE, db_index=True, related_name="tracking_points")
    label = models.CharField(max_length=64, blank=False, db_index=True)
    date = models.DateField(blank=False, null=False, auto_now=True)
    value = models.FloatField()
