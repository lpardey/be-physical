from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from . import bmi

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
            return bmi.get_bmi(self.height, latest_weight)

        return None

    @property
    def category_name_by_bmi(self) -> str | None:
        if self.bmi is None:
            return None

        return _(bmi.get_category_name(self.bmi))

    def __str__(self) -> str:
        return _(f"User #{self.user_id} information")


class StatusChoices(models.IntegerChoices):
    INACTIVE = 0, _("Inactive")
    ACTIVE = 1, _("Active")


class ScopeChoices(models.IntegerChoices):
    USER = 0, _("User")
    TRAINER = 1, _("Trainer")


class AnnotationTypeChoices(models.IntegerChoices):
    GENERAL = 0, _("General")
    GOAL = 1, _("Goal")
    RESTRICTION = 2, _("Restriction")
    TRAINER_ANNOTATION = 3, _("Trainer Annotation")


class UserAnnotation(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="annotations")
    text = models.TextField(max_length=500)
    annotation_type = models.IntegerField(choices=AnnotationTypeChoices, default=AnnotationTypeChoices.GENERAL)
    scope = models.IntegerField(choices=ScopeChoices, default=ScopeChoices.USER)
    status = models.IntegerField(choices=StatusChoices, default=StatusChoices.ACTIVE)

    def __str__(self) -> str:
        return f"{self.annotation_type}: {self.text}"


class UserTrackingPoint(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE, db_index=True, related_name="tracking_points")
    label = models.CharField(max_length=64, db_index=True)
    date = models.DateField(auto_now=True)
    value = models.FloatField()

    def __str__(self) -> str:
        return f"{self.date}: {self.label} --> {self.value}"
