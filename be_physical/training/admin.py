from django.contrib import admin
from django.db import models

from .models import Diet, Equipment, Exercise, Muscle, Routine, Training, Workout


class WorkoutInline(admin.TabularInline[Workout, models.Model]):
    model = Workout
    extra = 0


class RoutineInline(admin.TabularInline[Routine, models.Model]):
    model = Routine
    extra = 0


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin[Training]):
    list_display = ("user_info", "name", "type", "start_date", "due_date", "duration", "difficulty_level")
    inlines = [WorkoutInline]
    list_filter = ("type", "start_date", "due_date")
    search_fields = ("user_info__user__username", "name")


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin[Workout]):
    list_display = ("training", "name", "difficulty_level", "intensity")
    inlines = [RoutineInline]
    list_filter = ("difficulty_level", "intensity")
    search_fields = ("name", "training.name")


@admin.register(Muscle)
class MuscleAdmin(admin.ModelAdmin[Muscle]):
    list_display = ("name", "location", "action", "muscle_group")
    list_filter = ("muscle_group",)
    search_fields = ("name", "location", "action")


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin[Equipment]):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin[Exercise]):
    list_display = ("name", "difficulty_level", "repetition_duration", "image_url", "video_url")
    list_filter = ("difficulty_level",)
    search_fields = ("name", "description")


@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin[Routine]):
    list_display = ("workout_index", "sets", "repetitions", "sets_rest", "routine_rest", "routine_duration")
    list_filter = ("workout__training__user_info__user__username",)
    search_fields = ("exercise__name", "workout__name", "workout_index")


@admin.register(Diet)
class DietAdmin(admin.ModelAdmin[Diet]):
    pass
