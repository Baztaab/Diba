"""Common domain models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PlaceInput(BaseModel):
    """Input model for geographic place coordinates."""

    lat: float
    lon: float
    altitude: float = 0.0


class BirthData(BaseModel):
    """Input model for localized birth datetime and place."""

    year: int
    month: int
    day: int
    hour: int
    minute: int
    seconds: float = 0.0
    tz_str: str
    place: PlaceInput


class RuntimePolicy(BaseModel):
    """Runtime settings for ayanamsa, houses, and node mode."""

    ayanamsa_id: str = Field(default="lahiri")
    house_system_id: str = Field(default="whole_sign")
    node_mode: str = Field(default="mean")


class Meta(BaseModel):
    """Reproducibility metadata attached to public payloads."""

    engine_version: str
    swisseph_version: str
    config_digest: str
    ephe_expectations: str
    timezone_policy: str = "UTC"
