class Armor:
    def __init__(self, title, attack, defence, speed):
        self.title = title
        self.base_attack = attack
        self.base_defence = defence
        self.base_speed = speed
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.upgrades = []

    def upgrade(self, upgrade_card):
        """Upgrades the armor"""
        self.upgrades.append(upgrade_card)
        self.adjust_stats()

    def adjust_stats(self):
        """Adds up the base stats and any upgrades."""
        self.attack = self.base_attack + sum([upgrade.attack for upgrade in self.upgrades])
        self.defence = self.base_defence + sum([upgrade.defence for upgrade in self.upgrades])
        self.speed = self.base_speed + sum([upgrade.speed for upgrade in self.upgrades])

    def __repr__(self):
        upgrade_string = ", ".join(u.title for u in self.upgrades) + " "
        return "({}) {}{}:\n\tAttack: {}\n\tDefence: {}\n\tSpeed: {}".format(self.__class__.__name__, upgrade_string,
                                                                             self.title, self.attack, self.defence,
                                                                             self.speed)

    def __bool__(self):
        if self.title == "":
            return False
        return True
