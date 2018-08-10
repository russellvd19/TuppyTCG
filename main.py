import csv

from creature import Creature
from armor import Armor
from weapon import Weapon
from upgrade import Upgrade

creature_cards = {}
armor_cards = {}
weapon_cards = {}
upgrade_cards = {}


def run():
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


def import_data():
    with open("creatures.csv", "r") as in_file:
        csv_reader = csv.DictReader(in_file, quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            creature_cards[row["title"]] = Creature(row["title"], row["attack"], row["defence"], row["speed"])

    with open("armors.csv", "r") as in_file:
        csv_reader = csv.DictReader(in_file, quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            armor_cards[row["title"]] = Armor(row["title"], row["attack"], row["defence"], row["speed"])

    with open("weapons.csv", "r") as in_file:
        csv_reader = csv.DictReader(in_file, quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            weapon_cards[row["title"]] = Weapon(row["title"], row["attack"], row["defence"], row["speed"])

    with open("upgrades.csv", "r") as in_file:
        csv_reader = csv.DictReader(in_file, quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            upgrade_cards[row["title"]] = Upgrade(row["title"], row["attack"], row["defence"], row["speed"])


if __name__ == "__main__":
    import_data()
    run()
