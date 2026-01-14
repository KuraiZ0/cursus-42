class ArtifactCard:
    def __init__(
            self, name: str,
            cost: int, rarity: str, durability: int, effect: str):
        self.name = name
        self.cost = cost
        self.rarity = rarity
        self.durability = durability
        self.effect = effect

    def play(self, game_state: dict) -> dict:
        result = {
            'card_played': self.name,
            'mana_used': self.cost,
            'effect': f'Permanent: {self.effect}'
        }
        game_state['mana'] -= self.cost
        game_state['artifacts'].append(self.name)
        return result

    def activate_ability(self) -> dict:
        self.durability -= 1
        return {
            'activated': self.name, 'remaining_durability': self.durability}
