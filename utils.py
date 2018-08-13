import csv
import random
from math import ceil
from copy import deepcopy
from ast import literal_eval

import texttable
from creature import Creature
from armor import Armor
from weapon import Weapon
from upgrade import Upgrade


def print_all_cards(creature_cards, armor_cards, weapon_cards, upgrade_cards):
    """Prints all of the cards currently existing"""
    for deck_title, deck in [("Creature cards", creature_cards), ("\nArmor cards", armor_cards),
                             ("\nWeapon cards", weapon_cards), ("\nUpgrade cards", upgrade_cards)]:

        print(deck_title)
        card_list = list(deck.values())
        card_list.sort(key=lambda x: x.name)
        for index in range(int(ceil(len(card_list) / 5))):
            print_cards(card_list[index * 5:(index + 1) * 5])


def print_cards(card_list):
    """Prints all of the cards given into a texttable"""
    table = texttable.Texttable(max_width=0)
    table.add_row([repr(card) for card in card_list])
    print(table.draw() + "\n")


def make_deck(creature_cards, armor_cards, weapon_cards, upgrade_cards, deck_size=40):
    """Creates and returns a shuffled deck of length deck_size"""
    if deck_size < 10:
        return None

    card_list = list(creature_cards.values())
    creatures = [deepcopy(random.choice(card_list)) for _ in range((deck_size // 2) + 1)]

    card_list = list(armor_cards.values())
    armors = [deepcopy(random.choice(card_list)) for _ in range((deck_size // 6) + 1)]

    card_list = list(weapon_cards.values())
    weapons = [deepcopy(random.choice(card_list)) for _ in range((deck_size // 6) + 1)]

    card_list = list(upgrade_cards.values())
    upgrades = [deepcopy(random.choice(card_list)) for _ in range((deck_size // 6) + 1)]

    complete_deck = creatures + armors + weapons + upgrades
    while len(complete_deck) > deck_size:
        complete_deck.remove(random.choice(complete_deck))

    random.shuffle(complete_deck)
    return complete_deck


def import_data():
    """Loads all csv files of cards"""
    creature_cards = {}
    with open("../data/creatures.csv", "r") as in_file:
        csv_reader = csv.DictReader(in_file, quoting=csv.QUOTE_NONNUMERIC)
        unnamed_count = 0
        for row in csv_reader:
            # Creature(name, creature_type, energy, health, attack)
            name = row["name"]
            if name is None or name == "":
                name = "Creature{}".format(unnamed_count)
                unnamed_count += 1
            creature_cards[name] = Creature(name, row["type"], row["energy"], row["health"], row["attack"])

    armor_cards = {}
    with open("../data/armors.csv", "r") as in_file:
        csv_reader = csv.DictReader(in_file, quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            # Armor(name, attack, damage_negation_per_combat, max_damage_negation)
            armor_cards[row["name"]] = Armor(row["name"], row["attack"], row["damage_negation_per_combat"],
                                             row["max_damage_negation"])

    weapon_cards = {}
    with open("../data/weapons.csv", "r") as in_file:
        csv_reader = csv.DictReader(in_file, quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            # Weapon(name, attack, max_uses)
            weapon_cards[row["name"]] = Weapon(row["name"], row["attack"], row["max_uses"])

    upgrade_cards = {}
    with open("../data/upgrades.csv", "r") as in_file:
        csv_reader = csv.DictReader(in_file, quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            # Upgrade(name, upgrades)
            upgrade_cards[row["name"]] = Upgrade(row["name"], literal_eval(row["upgrades"]))

    return creature_cards, armor_cards, weapon_cards, upgrade_cards
