from datetime import date

from pydantic import BaseModel, EmailStr, PositiveFloat


class UserInfoSchema(BaseModel):
    username: str
    email: EmailStr
    birth_date: date
    creation_date: date


class BiometricsSchema(BaseModel):
    height: PositiveFloat
    weight: PositiveFloat | None
    desired_weight: PositiveFloat | None
    bmi: PositiveFloat | None
    bmi_category: str | None


class TrackingPointSchema(BaseModel):
    label: str
    description: str
    date: date
    value: PositiveFloat | None


class TrackingPointsData(BaseModel):
    tracking_points: list[TrackingPointSchema] | None
