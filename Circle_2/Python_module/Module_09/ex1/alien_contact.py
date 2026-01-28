"""Alien Contact Log Validation module."""
from typing import Self, Optional
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from enum import Enum


class ContactType(Enum):
    """Enumeration for alien contact types."""

    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    """Represent an alien contact report with validation.

    Attributes:
        contact_id: Unique ID starting with 'AC'.
        timestamp: Time of contact.
        location: Location string.
        contact_type: Type of contact (Enum).
        signal_strength: Float 0-10.
        duration_minutes: Duration in minutes.
        witness_count: Number of witnesses.
        message_received: Optional message content.
        is_verified: Verification status.
    """

    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def verify_data(self) -> Self:
        """Validate complex business rules for contacts."""
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC" (Alien Contact)')
        elif (self.contact_type == ContactType.PHYSICAL
                and not self.is_verified):
            raise ValueError("Physical contact reports must be verified")
        elif (self.contact_type == ContactType.TELEPATHIC
                and self.witness_count < 3):
            raise ValueError("Telepathic contact requires at least 3 witness")
        elif (self.signal_strength > 7.0 and not self.message_received):
            raise ValueError(
                "Strong signals (>7.0) should include received messages")
        return self


if __name__ == "__main__":
    print("Alien Contact Log Validation")
    print("======================================")
    alien = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime.now(),
        location="Area 51, Nevada",
        contact_type=ContactType.RADIO,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greatings from Zeta Reticuli"
        )
    try:
        print("Valid contact report:")
        print(f"ID: {alien.contact_id}")
        print(f"Type: {alien.contact_type}")
        print(f"Location: {alien.location}")
        print(f"Signal: {alien.signal_strength}/10")
        print(f"Duration: {alien.duration_minutes} minutes")
        print(f"Witnesses: {alien.witness_count}")
        print(f"Message: {alien.message_received}\n")
    except ValueError as ve:
        print(ve)
    print("======================================")
    print("Expected validation error:")
    try:
        wrong_alien = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=1,
            message_received="Greatings from Zeta Reticuli"
        )
    except ValueError as ve:
        print(ve)
