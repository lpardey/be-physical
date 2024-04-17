import datetime

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext as _


class DifficultyLevelChoices(models.IntegerChoices):
    BEGINNER = 0, _("Beginner")
    INTERMEDIATE = 1, _("Intermediate")
    ADVANCED = 2, _("Advanced")
    SPECIAL = 3, _("Special")


class Training(models.Model):
    user_info = models.ForeignKey("user_info.UserInfo", on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)  # crossfit, hiit, recovery
    difficulty_level = models.IntegerField(choices=DifficultyLevelChoices, default=DifficultyLevelChoices.BEGINNER)
    start_date = models.DateField(default=datetime.date.today)
    due_date = models.DateField(validators=[MinValueValidator(start_date)])

    diets: models.QuerySet["Diet"]
    workouts: models.QuerySet["Workout"]

    @cached_property
    def duration(self) -> datetime.timedelta:
        duration_delta = self.due_date - self.start_date
        return duration_delta

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
    # muscle_groups
    intensity = models.IntegerField(choices=IntensityChoices, default=IntensityChoices.LOW)
    difficulty_level = models.IntegerField(choices=DifficultyLevelChoices, default=DifficultyLevelChoices.BEGINNER)
    # duration = models.DurationField()
    # schedule: Schedule
    exercises: models.QuerySet["Exercise"]
    # training_sessions: models.QuerySet["TrainingSession"]


class MuscleGroupChoices(models.IntegerChoices):
    NECK = 0, _("Neck")
    BACK = 1, _("Back")
    SHOULDER = 2, _("Shoulder")
    ARM = 3, _("Arm")
    WRIST = 4, _("Wrist")
    HAND = 5, _("Hand")
    ABDOMEN = 6, _("Abdomen")
    HIP = 7, _("Hip")
    UPPER_LEG_AND_KNEE = 8, _("Upper_Leg_And_Knee")
    LOWER_LEG_AND_FOOT = 9, _("Lower_Leg_And_Foot")
    SPECIAL = 10, _("Special")


class Exercise(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=144, blank=True)
    difficulty_level = models.IntegerField(choices=DifficultyLevelChoices, default=DifficultyLevelChoices.BEGINNER)
    repetition_time = models.FloatField(validators=[MinValueValidator(0)])
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="exercises")
    tracking_label = models.ForeignKey("user_info.UserTrackingLabel", on_delete=models.CASCADE)
    muscle_groups = models.IntegerField(choices=MuscleGroupChoices, default=MuscleGroupChoices.UPPER_LEG_AND_KNEE)
    muscles_involved: models.QuerySet["Muscle"]
    equipment: models.QuerySet["Equipment"]
    image_url = models.URLField()
    video_url = models.URLField()
    repetition_time = models.FloatField(validators=[MinValueValidator(1)])


class Routine(models.Model):
    workout_index = models.IntegerField(auto_created=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    sets = models.FloatField()
    repetitions = models.FloatField()
    series_rest = models.FloatField()
    end_of_workload_rest = models.FloatField()

    @cached_property
    def estimated_workload_duration(self) -> float:
        exercise_duration = self.sets * self.repetitions * self.exercise.repetition_time + self.end_of_workload_rest
        rest_duration = (self.sets - 1) * self.series_rest
        duration = exercise_duration + rest_duration
        return duration


class Muscle(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    # Location and action may be scrape from https://en.wikipedia.org/wiki/List_of_skeletal_muscles_of_the_human_body
    location = models.CharField(max_length=100)
    action = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Diet(models.Model):
    pass
