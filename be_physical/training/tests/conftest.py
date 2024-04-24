import datetime

import pytest

from ...user_info.models import UserInfo
from ..models import Routine, Training, Workout


@pytest.fixture
def basic_training(basic_user_info: UserInfo, db: None) -> Training:
    data = {
        "user_info": basic_user_info,
        "name": "training_1",
        "type": "conditioning",
        "due_date": datetime.date.today + datetime.timedelta(days=30),
    }
    training = Training.objects.create(**data)
    return training


@pytest.fixture
def basic_workout(basic_training: Training, routine: Routine, db: None) -> Workout:
    data = {"training": basic_training, "name": "leg day", "description": "no pain, no gain", "routines": routine}
    workout = Workout.objects.create(**data)
    return workout
