import datetime

from django.forms import ValidationError
from django.utils.translation import gettext as _


def validate_due_date(value: datetime.date) -> None:
    if value < datetime.date.today():
        raise ValidationError(_("Due date must be in the future."))
