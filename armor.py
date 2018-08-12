class Armor:
    def __init__(self, title, attack, damage_negation_per_combat, max_damage_negation):
        self.title = title
        self.base_attack = attack
        self.base_damage_negation_per_combat = damage_negation_per_combat
        self.base_max_damage_negation = max_damage_negation
        self.attack = attack
        self.damage_negation_per_combat = damage_negation_per_combat
        self.max_damage_negation = max_damage_negation
        self.damage_negated = 0
        self.upgrades = []

    def upgrade(self, upgrade_card):
        """Upgrades the armor"""
        self.upgrades.append(upgrade_card)
        self.title = "{}, {}".format(upgrade_card.title, self.title)
        self.adjust_stats()

    def adjust_stats(self):
        """Adds up the base stats and any upgrades."""
        self.attack = self.base_attack + sum([upgrade.attack for upgrade in self.upgrades])
        self.damage_negation_per_combat = self.base_damage_negation_per_combat + sum(
            [upgrade.damage_degation_per_combat for upgrade in self.upgrades])
        self.max_damage_negation = self.base_max_damage_negation + sum(
            [upgrade.max_damage_negation for upgrade in self.upgrades])

    def amount_negated(self, damage):
        return min(self.damage_negation_per_combat, self.max_damage_negation - self.damage_negated)

    def is_destroyed(self):
        return self.damage_negated >= self.max_damage_negation

    def __repr__(self):
        return "({}) {}:\n\tAttack: {}\n\tDamage Negation: {}/combat\n\tDurability: {} / {}".format(
            self.__class__.__name__, self.title, self.attack, self.damage_negation_per_combat, self.damage_negated,
            self.max_damage_negation)

    def __bool__(self):
        if self.title == "":
            return False
        return True
