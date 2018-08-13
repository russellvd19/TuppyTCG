from armor import Armor
from weapon import Weapon
from creature_type import CreatureType


class Creature:
    def __init__(self, name, creature_type, energy, health, attack):
        self.name = name
        self.creature_type = CreatureType(creature_type)
        self.energy = energy
        self.base_health = health
        self.base_attack = attack
        self.health = health
        self.attack = attack
        self.weapon = Weapon("", 0, 0)
        self.armor = Armor("", 0, 0, 0)
        self.damage_negation = 0

    def equip_armor(self, new_armor):
        """Equips the new armor to this creature and adjusts any stat changes"""
        if new_armor == self.armor:
            return None
        old_armor = self.armor
        self.armor = new_armor
        self.adjust_stats()
        return old_armor

    def equip_weapon(self, new_weapon):
        """Equips the new weapon to this creature and adjusts any stat changes"""
        if new_weapon == self.weapon:
            return None
        old_weapon = self.weapon
        self.weapon = new_weapon
        self.adjust_stats()
        return old_weapon

    def adjust_stats(self):
        """Adds up the stats from weapon, armor, and all upgrades"""
        self.attack = self.base_attack + self.weapon.attack + self.armor.attack
        self.damage_negation = self.armor.damage_negation_per_combat

        self.attack = max(self.attack, 0)

    def is_dead(self):
        pass

    def take_damage(self, amount):
        pass

    def completed_attack(self):
        pass

    def value(self):
        pass

    def __repr__(self):
        return "({}) [{}] {}:\n  Health: {}\n  Attack: {}\n  Damage Negation: {}".format(self.__class__.__name__,
                                                                                         self.creature_type, self.name,
                                                                                         self.health,
                                                                                         self.attack,
                                                                                         self.damage_negation)

    def __bool__(self):
        if self.name == "":
            return False
        return True
