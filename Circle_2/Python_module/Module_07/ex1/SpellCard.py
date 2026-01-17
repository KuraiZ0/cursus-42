from abc import abstractmethod


class SpellCard:
    def __init__(self, name: str, cost: int, rarity: str, effect_type: str):
        self.name = name
        self.cost = cost
        self.rarity = rarity
        self.effect_type = effect_type

    @abstractmethod
    def play(self, game_state: dict) -> dict:
        result = {
            'card_played': self.name,
            'mana_used': self.cost,
            'effect': f'Deal {self.cost} damage to target'  # ← Ligne changée
        }
        game_state['mana'] -= self.cost
        return result

    def resolve_effect(self, targets: list) -> dict:
        return (
            {'target_affected': len(targets), 'effect_type': self.effect_type})
