"""Package initialization for the Ability System."""


from ex0.Card import Card
from .Combatable import Combatable
from .Magical import Magical
from .EliteCard import EliteCard

__all__: list[str] = [
    "Card",
    "Combatable",
    "Magical",
    "EliteCard"
]
