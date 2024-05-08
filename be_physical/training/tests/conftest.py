import datetime
from typing import Any

import pytest

# from be_physical.user_info.models import UserTrackingLabel
# import be_physical.user_info.tests.conftest  # noqa
from ..models import (
    DifficultyLevelChoices,
    Equipment,
    Exercise,
    IntensityChoices,
    Muscle,
    MuscleGroupChoices,
    Routine,
    Training,
    Workout,
)


@pytest.fixture
def workout_data() -> dict[str, Any]:
    data = {
        "name": "leg day",
        "description": "no pain, no gain",
        "difficulty_level": DifficultyLevelChoices.INTERMEDIATE,
        "intensity": IntensityChoices.INTERMEDIATE,
    }
    return data


@pytest.fixture
def routine_data() -> dict[str, Any]:
    data = {
        "workout_index": 0,
        "sets": 3,
        "repetitions": 6,
        "sets_rest": 1,
        "routine_rest": 2,
    }
    return data


@pytest.fixture
def training_data(basic_user_info) -> dict[str, Any]:
    data = {
        "user_info": basic_user_info,
        "name": "training_1",
        "type": "conditioning",
        "due_date": datetime.date.today() + datetime.timedelta(days=30),
    }
    return data


@pytest.fixture
def muscle_data() -> dict[str, Any]:
    data = {
        "name": "quadriceps femoris",
        "location": "Lower limb, Thigh, Posterior compartment/hamstring ",
        "action": "	Knee extension; Hip flexion ",
        "muscle_group": MuscleGroupChoices.UPPER_LEG_AND_KNEE,
    }
    return data


@pytest.fixture
def exercise_data(training_tracking_label) -> dict[str, Any]:
    data = {
        "name": "Barbell Back Squat",
        "description": " strength exercise in which the trainee lowers their hips from a standing position and then stands back up.",
        "difficulty_level": DifficultyLevelChoices.INTERMEDIATE,
        "repetition_duration": 4,
        "image_url": "image.com",
        "video_url": "video.com",
        "tracking_label": training_tracking_label,
    }
    return data


@pytest.fixture
def complete_training(
    training_data: dict[str, Any],
    workout_data: dict[str, Any],
    routine_data: dict[str, Any],
    muscle_data: dict[str, Any],
    exercise_data: dict[str, Any],
    db: None,
) -> Training:
    training = Training.objects.create(**training_data)
    workout = Workout.objects.create(training=training, **workout_data)
    Equipment.objects.create(name="Olympic Barbell", description="Made of steel for extreme workouts")
    Muscle.objects.create(**muscle_data)
    exercise = Exercise.objects.create(**exercise_data)
    Routine.objects.create(exercise=exercise, workout=workout, **routine_data)
    return training


@pytest.fixture
def basic_workout(training_data: dict[str, Any], workout_data: dict[str, Any], db: None) -> dict[str, Any]:
    training = Training.objects.create(**training_data)
    workout = Workout.objects.create(training=training, **workout_data)
    return workout


@pytest.fixture
def basic_routine(basic_exercise: Exercise, basic_workout: Workout, db: None) -> Workout:
    data = {
        "workout_index": 0,
        "exercise": basic_exercise,
        "workout": basic_workout,
        "sets": 3,
        "repetitions": 6,
        "sets_rest": 1,
        "routine_rest": 2,
    }
    routine = Routine.objects.create(**data)
    return routine


@pytest.fixture
def basic_equipment(db: None) -> Equipment:
    data = {"name": "Olympic Barbell", "description": "Made of steel for extreme workouts"}
    equipment = Equipment.objects.create(**data)
    return equipment


@pytest.fixture
def basic_muscle(muscle_data: dict[str, Any], db: None) -> Muscle:
    muscle = Muscle.objects.create(**muscle_data)
    return muscle


@pytest.fixture
def basic_exercise(exercise_data, db: None) -> Exercise:
    exercise = Exercise.objects.create(**exercise_data)
    return exercise
