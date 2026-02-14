"""Space Crew Management module."""
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum


class Rank(Enum):
    """Enumeration rank for space crew."""

    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    """Represent a single crew member validation."""

    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    """Represent a space mission with nested crew validation."""

    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def verify_data(self):
        """Validate mission safety requirements."""
        leadership: bool = any(
            m.rank in (Rank.COMMANDER, Rank.CAPTAIN) for m in self.crew)
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')
        elif not leadership:
            raise ValueError("Must have at least one Commander or Captain")
        elif not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        if self.duration_days > 365:
            experienced_count: int = sum(
                1 for m in self.crew if m.years_experience >= 5
            )
            if experienced_count < len(self.crew) / 2:
                raise ValueError(
                    "Long missions (> 365 days) need 50% experienced crew "
                    "(5+ years)"
                )

        return self


if __name__ == "__main__":
    print("Space Mission Crew Validation")
    print("=========================================")
    sarah = CrewMember(
        member_id="S_001",
        name="Sarah Connor",
        rank=Rank.COMMANDER,
        age=34,
        specialization="Strategy",
        years_experience=6,
        is_active=True
    )
    john = CrewMember(
        member_id="J_001",
        name="John Smith",
        rank=Rank.LIEUTENANT,
        age=42,
        specialization="Armory",
        years_experience=3,
        is_active=True
    )
    alice = CrewMember(
        member_id="A_001",
        name="Alice Johnson",
        rank=Rank.OFFICER,
        age=27,
        specialization="Hacking",
        years_experience=7,
        is_active=True
    )
    crew_list: list[CrewMember] = [sarah, john, alice]
    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime.now(),
        duration_days=900,
        crew=crew_list,
        budget_millions=2500.0
    )
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(crew_list)}")
    print("Crew members:")
    for member in crew_list:
        print(
            f" - {member.name} ({member.rank.name}) - {member.specialization}")
    print()
    print("=========================================")
    wrong_sarah = CrewMember(
        member_id="S_001",
        name="Sarah Connor",
        rank=Rank.CADET,
        age=34,
        specialization="Strategy",
        years_experience=6,
        is_active=True
    )
    print("Expected validation error:")
    wrong_crew_list: list[CrewMember] = [wrong_sarah, alice, john]
    try:
        wrong_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            crew=wrong_crew_list,
            budget_millions=2500.0
        )
    except ValidationError as ve:
        print(ve)
