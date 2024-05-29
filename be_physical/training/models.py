from __future__ import annotations

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
    type = models.CharField(max_length=50, blank=True)  # crossfit, hiit, recovery
    start_date = models.DateField(default=datetime.date.today)
    due_date = models.DateField(validators=[MinValueValidator(start_date)])
    # user_training_goals (marzo quiero estar en 80 kilos)

    workouts: models.QuerySet[Workout]
    diets: models.QuerySet[Diet]  # Offer personalized meal plans based on dietary preferences.

    @cached_property
    def duration(self) -> datetime.timedelta:
        result = self.due_date - self.start_date
        return result

    @cached_property
    def muscles(self) -> set[Muscle]:
        result = {muscle for workout in self.workouts.all() for muscle in workout.muscles}
        return result

    @cached_property
    def muscle_groups(self) -> set[MuscleGroupChoices]:
        result = {MuscleGroupChoices(muscle.muscle_group) for muscle in self.muscles}
        return result

    @cached_property
    def difficulty_level(self) -> DifficultyLevelChoices | None:
        difficulty_levels = self.workouts.values_list("difficulty_level", flat=True)

        if not difficulty_levels:
            return None

        average_value = sum(difficulty_levels) / len(difficulty_levels)
        level = DifficultyLevelChoices(round(average_value))
        return level

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
    # workout_goal
    difficulty_level = models.IntegerField(choices=DifficultyLevelChoices, default=DifficultyLevelChoices.BEGINNER)
    intensity = models.IntegerField(choices=IntensityChoices, default=IntensityChoices.LOW)
    routines: models.QuerySet[Routine]

    @property
    def muscles(self) -> set[Muscle]:
        result = {muscle for routine in self.routines.all() for muscle in routine.exercise.muscles.all()}
        return result

    @property
    def muscle_groups(self) -> set[MuscleGroupChoices]:
        result = {MuscleGroupChoices(muscle.muscle_group) for muscle in self.muscles}
        return result


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


class Muscle(models.Model):
    name = models.CharField(max_length=50)
    # Location and action may be scrape from https://en.wikipedia.org/wiki/List_of_skeletal_muscles_of_the_human_body
    location = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    muscle_group = models.IntegerField(choices=MuscleGroupChoices, default=MuscleGroupChoices.UPPER_LEG_AND_KNEE)
    exercises: models.QuerySet[Exercise]

    def __str__(self) -> str:
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=144, blank=True)
    difficulty_level = models.IntegerField(choices=DifficultyLevelChoices, default=DifficultyLevelChoices.BEGINNER)
    repetition_duration = models.IntegerField(validators=[MinValueValidator(1)])
    muscles = models.ManyToManyField(Muscle, related_name="exercises")
    image_url = models.URLField()
    video_url = models.URLField()
    tracking_label = models.ForeignKey("user_info.UserTrackingLabel", on_delete=models.CASCADE)  # TODO Check
    equipment = models.ManyToManyField(Equipment)
    routines: models.QuerySet[Routine]

    @cached_property
    def muscle_groups(self) -> set[MuscleGroupChoices]:
        query_result = self.muscles.values_list("muscle_group", flat=True).distinct()
        return set(query_result)


class Routine(models.Model):
    workout_index = models.IntegerField()  # This will allow to organize at will the workouts
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="routines")
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="routines")
    sets = models.IntegerField()
    repetitions = models.IntegerField()
    sets_rest = models.IntegerField()
    routine_rest = models.IntegerField()

    @cached_property
    def routine_duration(self) -> int:
        exercise_duration = self.sets * self.repetitions * self.exercise.repetition_duration
        rest_duration = (self.sets - 1) * self.sets_rest + self.routine_rest
        result = exercise_duration + rest_duration
        return result


class Diet(models.Model):
    pass
