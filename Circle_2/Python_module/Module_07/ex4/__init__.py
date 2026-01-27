"""
This module provides the necessary classes for running a tournament.

It includes the `TournamentCard`, `Rankable`, and `TournamentPlatform`
classes.
"""
from ex0.Card import Card
from ex2.Combatable import Combatable
from .Rankable import Rankable
from .TournamentCard import TournamentCard
from .TournamentPlatform import TournamentPlatform

__all__: list[str] = [
    "Card",
    "Combatable",
    "TournamentCard",
    "Rankable",
    "TournamentPlatform"
]
