import datetime

# from django.utils.functional import cached_property
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _


class LevelChoices(models.IntegerChoices):
    BEGINNER = 0, _("Beginner")
    INTERMEDIATE = 1, _("Intermediate")
    ADVANCE = 2, _("Advance")
    SPECIAL = 3, _("Special")


class Training(models.Model):
    user_info = models.ForeignKey("user_info.UserInfo", on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)  # crossfit, hiit, recovery
    level = models.IntegerField(choices=LevelChoices, default=LevelChoices.BEGINNER)
    start_date = models.DateField(default=datetime.date.today)
    due_date = models.DateField(validators=[MinValueValidator(start_date)])
    duration = models.DurationField()
    diets: models.QuerySet["Diet"]
    workouts: models.QuerySet["Workout"]
    training_goals: models.QuerySet[
        "TrainingGoal"
    ]  # metrica: se puede usar el modelo de tracking point  Ej: para el 18 de marzo quiero estar en 80 kg

    # @cached_property
    # def duration(self) -> int:
    #     duration_delta = self.due_date - self.start_date
    #     return duration_delta.days

    @property
    def streak(self) -> None:
        pass

    def __str__(self) -> str:
        return _(f"{self.name}")


class IntensityChoices(models.IntegerChoices):
    LOW = 0, _("Low")
    INTERMEDIATE = 1, _("Intermediate")
    HIGH = 2, _("High")
    SPECIAL = 3, _("Special")


class Workout(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name="workouts")
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=144, blank=True)
    # muscles_involved
    goal = models.ForeignKey("TrainingGoal", on_delete=models.CASCADE, db_index=True)
    intensity = models.IntegerField(choices=IntensityChoices, default=IntensityChoices.LOW)
    level = models.IntegerField(choices=LevelChoices, default=LevelChoices.BEGINNER)
    duration = models.DurationField()
    # schedule: Schedule
    exercises: models.QuerySet["Exercise"]
    # training_sessions: models.QuerySet["TrainingSession"]


class TrainingGoal(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, db_index=True, related_name="training_goals")
    label = models.ForeignKey("TrainingGoalLabel", on_delete=models.CASCADE, db_index=True)
    date = models.DateField(default=datetime.date.today)
    value = models.FloatField()

    def __str__(self) -> str:
        return _(f"{self.date}: {self.label} --> {self.value}")


class TrainingGoalLabel(models.Model):
    label = models.CharField(max_length=64, primary_key=True)
    description = models.TextField(max_length=144, blank=True)

    def __str__(self) -> str:
        return _(f"{self.label}")


class Exercise(models.Model):
    pass


class TrainingSession(models.Model):
    pass


class Diet(models.Model):
    pass
