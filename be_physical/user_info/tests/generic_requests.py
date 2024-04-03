import datetime
import math
from dataclasses import dataclass
from typing import Any

from django.contrib.auth.models import User

from ..models import (
    AnnotationTypeChoices,
    ScopeChoices,
    StatusChoices,
    UserInfo,
    UserTrackingLabel,
)


@dataclass(frozen=True)
class TrackingPointRequest:
    user_info_exists: bool = True
    label_exists: bool = True
    date: datetime.date | str = datetime.date.today()
    value: float | str = 10.0

    def generate_data(self, basic_user_info: UserInfo, user_tracking_label: UserTrackingLabel) -> dict[str, Any]:
        return {
            "id": basic_user_info.user.pk,
            "user_info": basic_user_info.pk if self.user_info_exists else math.inf,
            "label": user_tracking_label.label if self.label_exists else math.inf,
            "date": str(self.date),
            "value": self.value,
        }


@dataclass(frozen=True)
class AnnotationRequest:
    user_info_exists: bool = True
    text: str = "Annotation text"
    annotation_type: AnnotationTypeChoices | str = AnnotationTypeChoices.GENERAL
    scope: ScopeChoices | str = ScopeChoices.USER
    status: StatusChoices | str = StatusChoices.ACTIVE

    def generate_data(self, basic_user_info: UserInfo) -> dict[str, Any]:
        return {
            "id": basic_user_info.user.pk,
            "user_info": basic_user_info.pk if self.user_info_exists else math.inf,
            "text": self.text,
            "annotation_type": self.annotation_type,
            "scope": self.scope,
            "status": self.status,
        }


@dataclass(frozen=True)
class TrackingLabelRequest:
    label: str = "Label"
    description: str = "Description"

    def generate_data(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "description": self.description,
        }


@dataclass(frozen=True)
class CreateUserInfoRequest:
    height: float | str = 1.86
    birth_date: datetime.date | str = datetime.date.fromisoformat("1989-09-01")

    def generate_data(self, user: User) -> dict[str, Any]:
        return {
            "user": user.pk,
            "height": str(self.height),
            "birth_date": str(self.birth_date),
        }
