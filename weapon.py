from card import Card


class Weapon(Card):
    def __init__(self, name, attack, max_uses):
        super().__init__()
        self.name = name
        self.base_attack = attack
        self.base_max_uses = max_uses
        self.attack = attack
        self.max_uses = max_uses
        self.uses = 0
        self.upgrades = []

    def upgrade(self, upgrade_card):
        """Upgrades the weapon"""
        self.upgrades.append(upgrade_card)
        self.name = "{}, {}".format(upgrade_card.name, self.name)
        self.adjust_stats()

    def adjust_stats(self):
        """Adds up the base stats and any upgrades."""
        self.attack = self.base_attack + sum([upgrade.attack for upgrade in self.upgrades])
        self.max_uses = self.base_max_uses + sum([upgrade.max_uses for upgrade in self.upgrades])

    def is_destroyed(self):
        if self:
            return self.uses >= self.max_uses
        return False

    def __repr__(self):
        return "({})\n{}:\n  Attack: {}\n  Uses left: {} / {}".format(self.__class__.__name__, self.name, self.attack,
                                                                     self.max_uses - self.uses, self.max_uses)

    def __bool__(self):
        if self.name == "":
            return False
        return True
