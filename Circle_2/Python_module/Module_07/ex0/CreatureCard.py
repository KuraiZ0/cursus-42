from Card import Card


class CreatureCard(Card):
    def __init__(
            self, name: str, cost: int, rarity: str, attack: int, health: int):
        super().__init__(name, cost, rarity)
        self.attack = attack
        self.health = health

    def play(self, game_state: dict) -> dict:
        return game_state

    def attack_target(self, target) -> dict:
        """Function to attack a predefined target"""
        if self.attack > 0 and self.health > 0:
            target.health -= self.attack
            return {
                "attacker": self.name,
                "target": target.name,
                "damage_dealt": self.attack,
                "combat_resolved": True
            }
        return target

    def get_stats(self) -> dict:
        result = self.get_card_info()
        result["attack"] = self.attack
        result["health"] = self.health
        return result
