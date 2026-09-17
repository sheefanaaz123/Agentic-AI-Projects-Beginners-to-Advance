
"""Validated input and output contracts for the assistant."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TravelRequest(BaseModel):
    """User's travel intent."""

    city: str = Field(min_length=1, max_length=120)
    travel_date: date
    interests: list[str] = Field(
        default_factory=list,
        max_length=10,
        description="Activities such as hiking, sightseeing, or beach.",
    )

    @field_validator("city")
    @classmethod
    def clean_city(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("City cannot be blank.")
        return value

    @field_validator("interests")
    @classmethod
    def clean_interests(cls, values: list[str]) -> list[str]:
        cleaned = [item.strip() for item in values if item.strip()]
        if any(len(item) > 80 for item in cleaned):
            raise ValueError("Each interest must be 80 characters or less.")
        return cleaned


class WeatherSummary(BaseModel):
    """Normalized weather facts for the requested day."""

    location: str
    travel_date: date
    temperature_min_c: float | None
    temperature_max_c: float | None
    weather_description: str
    precipitation_probability_percent: float | None
    precipitation_sum_mm: float | None
    wind_speed_max_kmh: float | None
    source: str = "Open-Meteo"


class TravelAdvice(BaseModel):
    """Machine-readable final travel report."""

    destination: str
    travel_date: date
    weather: WeatherSummary

    packing_list: list[str] = Field(min_length=1, max_length=12)
    outdoor_activity_assessment: str
    suggested_activities: list[str] = Field(max_length=8)
    safety_considerations: list[str] = Field(max_length=8)

    overall_summary: str
    confidence_note: str

    @field_validator("packing_list", "suggested_activities",
                     "safety_considerations")
    @classmethod
    def remove_blank_items(cls, values: list[str]) -> list[str]:
        cleaned = [item.strip() for item in values]
        if any(not item for item in cleaned):
            raise ValueError("List items cannot be blank.")
        return cleaned