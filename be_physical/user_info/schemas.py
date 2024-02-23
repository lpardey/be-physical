from datetime import date

from pydantic import BaseModel, EmailStr, PositiveFloat


class UserInfoSchema(BaseModel):
    username: str
    email: EmailStr
    birth_date: date
    creation_date: date


class PhysicalBiometricsSchema(BaseModel):
    height: PositiveFloat
    weight: PositiveFloat | None
    desired_weight: PositiveFloat | None
    bmi: PositiveFloat | None
    bmi_category: str | None
