from abc import abstractmethod
from ex0.Card import Card


class SpellCard(Card):
    def __init__(self, name: str, cost: int, rarity: str, effect_type: str):
        super().__init__(name, cost, rarity)
        self.effect_type = effect_type

    @abstractmethod
    def play(self, game_state: dict) -> dict:
        result = {
            'card_played': self.name,
            'mana_used': self.cost,
            'effect': f'{self.effect_type.capitalize()} effect applied'
        }
        game_state['mana'] -= self.cost
        return result

    def resolve_effect(self, targets: list) -> dict:
        return (
            {'target_affected': len(targets), 'effect_type': self.effect_type})
