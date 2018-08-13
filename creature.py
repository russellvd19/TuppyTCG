from card import Card
from armor import Armor
from weapon import Weapon
from creature_type import CreatureType


class Creature(Card):
    def __init__(self, name, creature_type, energy, health, attack):
        super().__init__()
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
        """Checks if this creature is dead"""
        return self.health <= 0

    def take_damage(self, amount):
        """Takes an amount of damage, decreased if there is appropriate armor"""
        if self.armor:
            amount = max(amount - self.armor.negate_damage(amount), 0)
        self.health -= amount
        return amount

    def completed_attack(self):
        """Returns all cards that have to be discarded and sent to unused"""
        to_discard = []
        to_unused = []

        if self.armor.is_destroyed():
            to_discard.append(self.armor)
            self.armor = Armor("", 0, 0, 0)

        if self.weapon.is_destroyed():
            to_discard.append(self.weapon)
            self.weapon = Weapon("", 0, 0)

        if self.is_dead():
            to_discard.append(self)
            if self.armor:
                to_unused.append(self.armor)
            if self.weapon:
                to_unused.append(self.weapon)

        return to_discard, to_unused

    def value(self):
        """Returns the shards and xp values of this creature"""
        return self.energy, self.energy * 5

    def __repr__(self):
        return "({}) [{}]\n{}:\n  Health: {}\n  Attack: {}\n  Damage Negation: {}".format(self.__class__.__name__,
                                                                                         self.creature_type, self.name,
                                                                                         self.health,
                                                                                         self.attack,
                                                                                         self.damage_negation)

    def __bool__(self):
        if self.name == "":
            return False
        return True
