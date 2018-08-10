from armor import Armor
from weapon import Weapon
from upgrade import Upgrade


class Creature:
    def __init__(self, title, attack, defence, speed):
        self.title = title
        self.base_attack = attack
        self.base_defence = defence
        self.base_speed = speed
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.weapon = Weapon("", 0, 0, 0)
        self.armor = Armor("", 0, 0, 0)
        self.upgrades = []

    def equip_armor(self, new_armor):
        """Equips the new armor to this creature and adjusts any stat changes"""
        old_armor = self.armor
        self.armor = new_armor
        self.adjust_stats()
        return old_armor

    def equip_weapon(self, new_weapon):
        """Equips the new weapon to this creature and adjusts any stat changes"""
        old_weapon = self.weapon
        self.weapon = new_weapon
        self.adjust_stats()
        return old_weapon

    def add_upgrade(self, new_upgrade):
        self.upgrades.append(new_upgrade)
        self.adjust_stats()

    def adjust_stats(self):
        """Adds up the stats from weapon, armor, and all upgrades"""
        self.attack = self.base_attack + self.weapon.attack + self.armor.attack + sum([upgrade.attack for upgrade in self.upgrades])
        self.defence = self.base_defence + self.weapon.defence + self.armor.defence + sum([upgrade.defence for upgrade in self.upgrades])
        self.speed = self.base_speed + self.weapon.speed + self.armor.speed + sum([upgrade.speed for upgrade in self.upgrades])

    def __repr__(self):
        return "{}:\n\tAttack: {}\n\tDefence: {}\n\tSpeed: {}".format(self.title, self.attack, self.defence, self.speed)
