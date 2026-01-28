"""Show usage of Pydantic Model."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    """Represent a space station with validated fields.

    Attributes:
        station_id: Unique identifier (3-10 chars).
        name: Station name (1-50 chars).
        crew_size: Number of crew members (1-20).
        power_level: Power percentage (0.0-100.0).
        oxygen_level: Oxygen percentage (0.0-100.0).
        last_maintenance: Timestamp of last check.
        is_operational: Status flag (default True).
        notes: Optional additional information.
    """

    station_id: str = Field(
        min_length=3, max_length=10, description="ID of the station")
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


if __name__ == "__main__":
    print("Space Station Data Validation")
    print("========================================")
    try:
        station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.now(),
            is_operational=True,
            notes="")
    except ValidationError as ve:
        print("Expected validation error:")
        print(ve)
    print("Valid station created:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size}")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(f"Date: {station.last_maintenance}")
    if station.is_operational:
        print("Status: Operational\n")
    else:
        print("Status: Not operational\n")
    print("========================================")
    print("Testing invalid station (Crew > 20)...")
    try:
        SpaceStation(
            station_id="DEATH_STAR",
            name="Too Big Station",
            crew_size=100,
            power_level=50.0,
            oxygen_level=50.0,
            last_maintenance=datetime.now()
        )
    except ValidationError as ve:
        print("Expected validation error:")
        print(ve)
