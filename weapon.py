class Weapon:
    def __init__(self, title, attack, max_uses):
        self.title = title
        self.base_attack = attack
        self.base_max_uses = max_uses
        self.attack = attack
        self.max_uses = max_uses
        self.uses = 0
        self.upgrades = []

    def upgrade(self, upgrade_card):
        """Upgrades the weapon"""
        self.upgrades.append(upgrade_card)
        self.title = "{}, {}".format(upgrade_card.title, self.title)
        self.adjust_stats()

    def adjust_stats(self):
        """Adds up the base stats and any upgrades."""
        self.attack = self.base_attack + sum([upgrade.attack for upgrade in self.upgrades])
        self.max_uses = self.base_max_uses + sum([upgrade.max_uses for upgrade in self.upgrades])

    def is_destroyed(self):
        return self.uses >= self.max_uses

    def __repr__(self):
        return "({}) {}:\n\tAttack: {}\n\tUses left: {} / {}".format(self.__class__.__name__, self.title, self.attack,
                                                                     self.max_uses - self.uses, self.max_uses)

    def __bool__(self):
        if self.title == "":
            return False
        return True
