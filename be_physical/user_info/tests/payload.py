import datetime
import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from ..models import (
    AnnotationTypeChoices,
    ScopeChoices,
    StatusChoices,
    UserInfo,
    UserTrackingLabel,
)


@dataclass(frozen=True)
class Payload(ABC):
    user_info_exists: bool = True

    @abstractmethod
    def generate_payload(self, basic_user_info: UserInfo, *args, **kwargs): ...


@dataclass(frozen=True)
class TrackingPointPayload(Payload):
    label_exists: bool = True
    date: datetime.date | str = datetime.date.today()
    value: float | str = 10.0

    def generate_payload(self, basic_user_info: UserInfo, user_tracking_label: UserTrackingLabel) -> dict[str, Any]:
        payload = {
            "user_info": basic_user_info.pk if self.user_info_exists else math.inf,
            "label": user_tracking_label.pk if self.label_exists else math.inf,
            "date": str(self.date),
            "value": self.value,
        }
        return payload


@dataclass(frozen=True)
class AnnotationPayload(Payload):
    text: str = "Annotation text"
    annotation_type: AnnotationTypeChoices | str = AnnotationTypeChoices.GENERAL
    scope: ScopeChoices | str = ScopeChoices.USER
    status: StatusChoices | str = StatusChoices.ACTIVE

    def generate_payload(self, basic_user_info: UserInfo) -> dict[str, Any]:
        payload = {
            "user_info": basic_user_info.pk if self.user_info_exists else math.inf,
            "text": self.text,
            "annotation_type": self.annotation_type,
            "scope": self.scope,
            "status": self.status,
        }
        return payload
