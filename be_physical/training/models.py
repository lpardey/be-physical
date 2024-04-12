import datetime

from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from be_physical.user_info.models import UserInfo


class TypeChoices(models.IntegerChoices):
    BEGINNER = 0, _("Beginner")
    INTERMEDIATE = 1, _("Intermediate")
    ADVANCE = 2, _("Advance")
    SPECIAL = 3, _("Special")


class Training(models.Model):
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)  # crossfit, hiit, recovery
    level = models.IntegerField(choices=TypeChoices, default=TypeChoices.BEGINNER)
    start_date = models.DateField(default=datetime.date.today)
    due_date = models.DateField()
    workouts: models.QuerySet["Workout"]
    # diets: models.QuerySet["Diet"]
    training_goals: models.QuerySet[
        "TrainingGoal"
    ]  # metrica: se puede usar el modelo de tracking point  Ej: para el 18 de marzo quiero estar en 80 kg

    @cached_property
    def duration(self) -> datetime.date:
        return self.due_date - self.start_date

    @property
    def streak(self):
        pass

    def __str__(self) -> str:
        return _(f"{self.name}")


class Workout(models.Model):
    pass


class TrainingGoal(models.Model):
    pass
