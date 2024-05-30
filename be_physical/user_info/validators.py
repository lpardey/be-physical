import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


# UserInfo model
def validate_birth_date(value: datetime.date) -> None:
    min_date_limit = datetime.date.today() - datetime.timedelta(days=36500)
    max_date = datetime.date.today()

    if not (min_date_limit <= value < max_date):
        raise ValidationError(_("Invalid date"))
