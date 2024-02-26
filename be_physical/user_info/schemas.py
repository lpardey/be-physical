from datetime import date

from pydantic import BaseModel, EmailStr, Field, PositiveFloat


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
    value: float | None = Field(ge=0)


class TrackingPointsData(BaseModel):
    tracking_points: list[TrackingPointSchema] | None


class AnnotationSchema(BaseModel):
    text: str
    annotation_type: int = Field(ge=0)
    scope: int = Field(ge=0)
    status: int = Field(ge=0)


class AnnotationsData(BaseModel):
    annotations: list[AnnotationSchema] | None
