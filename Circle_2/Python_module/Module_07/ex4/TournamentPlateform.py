"""Tournament Platform."""

from .TournamentCard import TournamentCard
from random import choice


class TournamentPlateform:
    def __init__(self, cards: dict = {}):
        self.cards = {}
        self.matches_count = 0

    def register_card(self, card: TournamentCard) -> str:
        self.cards[card.card_id] = card
        return f"{card.name} (ID: {card.card_id})!"

    def create_match(self, card1_id: str, card2_id: str) -> dict:
        """
        Simulate a match between two cards.

        Args:
            card1_id (str): ID of the first card.
            card2_id (str): ID of the second card.

        Returns:
            dict: The match results.
        """
        c1: TournamentCard = self.cards[card1_id]
        c2: TournamentCard = self.cards[card2_id]
        self.matches_count += 1

        if c1.attack_value > c2.attack_value:
            winner, loser = c1, c2
        elif c2.attack_value > c1.attack_value:
            winner, loser = c2, c1
        else:
            winner: TournamentCard = choice([c1, c2])
            loser: TournamentCard = c2 if winner == c1 else c1

        winner.update_wins(1)
        loser.update_losses(1)

        return {
            "winner": winner,
            "loser": loser,
            "winner_rating": winner.rating,
            "loser_rating": loser.rating
        }

    def get_leaderboard(self) -> list:
        """
        Generate a sorted leaderboard.

        Returns:
            list: List of strings describing the ranking.
        """
        def get_rating(card) -> int:
            return card.rating

        sorted_card: list[TournamentCard] = sorted(
            self.cards.values(), key=get_rating, reverse=True)
        leaderboard: list[str] = []
        for i, card in enumerate(sorted_card, 1):
            info: str = (f"{i}. {card.name}\n Rating:"
                         f" {card.rating} ({card.win}-{card.loose})")
            leaderboard.append(info)
        return leaderboard

    def generate_tournament_report(self) -> dict:
        """Generate a summary report of the platform status."""
        total_rating: int = sum(c.rating for c in self.cards.values())
        avg = total_rating / len(self.cards) if self.cards else 0

        return {
            "total_cards": len(self.cards),
            "matches_played": self.matches_count,
            "avg_rating": int(avg),
            "platform_status": "active"
        }
