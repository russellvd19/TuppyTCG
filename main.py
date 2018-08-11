import csv
import random
from copy import deepcopy
import texttable

from creature import Creature
from armor import Armor
from weapon import Weapon
from upgrade import Upgrade

creature_cards = {}
armor_cards = {}
weapon_cards = {}
upgrade_cards = {}


def run():
    p1_deck = make_deck()
    p1_hand = p1_deck[:5]
    print("Player 1's Hand")

    table = texttable.Texttable()
    table.header([""] + ["{}\n({})".format(card.title, type(card).__name__) for card in p1_hand])
    table.add_row(["Attack:"] + [card.attack for card in p1_hand])
    table.add_row(["Defence:"] + [card.defence for card in p1_hand])
    table.add_row(["Speed:"] + [card.speed for card in p1_hand])
    print(table.draw() + "\n")


def print_all_cards():
    """Prints all of the cards currently existing"""
    print("Creature cards")
    for creature in creature_cards.values():
        print(creature)

    print("\nArmor cards")
    for armor in armor_cards.values():
        print(armor)

    print("\nWeapon cards")
    for weapon in weapon_cards.values():
        print(weapon)

    print("\nUpgrade cards")
    for upgrade in upgrade_cards.values():
        print(upgrade)


def make_deck(deck_size=40):
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
    with open("data/creatures.csv", "r") as in_file:
        csv_reader = csv.DictReader(in_file, quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            creature_cards[row["title"]] = Creature(row["title"], row["attack"], row["defence"], row["speed"])

    with open("data/armors.csv", "r") as in_file:
        csv_reader = csv.DictReader(in_file, quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            armor_cards[row["title"]] = Armor(row["title"], row["attack"], row["defence"], row["speed"])

    with open("data/weapons.csv", "r") as in_file:
        csv_reader = csv.DictReader(in_file, quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            weapon_cards[row["title"]] = Weapon(row["title"], row["attack"], row["defence"], row["speed"])

    with open("data/upgrades.csv", "r") as in_file:
        csv_reader = csv.DictReader(in_file, quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            upgrade_cards[row["title"]] = Upgrade(row["title"], row["attack"], row["defence"], row["speed"])


if __name__ == "__main__":
    import_data()
    run()
