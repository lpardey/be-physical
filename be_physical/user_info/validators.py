import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


# UserInfo model
def validate_birth_date(value: datetime.date) -> datetime.date:
    min_date_limit = datetime.date(1900, 1, 1)
    max_date = datetime.date.today()

    if value > max_date or value < min_date_limit:
        raise ValidationError(_("Invalid date"))

    return value
