import csv
import random
from copy import deepcopy
import time

import texttable
from creature import Creature
from armor import Armor
from weapon import Weapon
from upgrade import Upgrade

creature_cards = {}
armor_cards = {}
weapon_cards = {}
upgrade_cards = {}

field = []
unused_items_on_field = []
discarded_cards = []
p1_hand = []


def run():
    global p1_hand
    p1_deck = make_deck()
    p1_hand = p1_deck[:5]
    print("Player 1's Hand")
    print_cards(p1_hand)

    while Creature not in [type(card) for card in p1_hand]:
        print("You're hand didn't have a creature. Redrawing...")
        random.shuffle(p1_deck)
        p1_hand = p1_deck[:5]
        print_cards(p1_hand)

    while True:
        get_user_action()


def print_cards(card_list):
    table = texttable.Texttable()
    table.header([""] + ["{}\n({})".format(card.title, type(card).__name__) for card in card_list])
    table.add_row(["Attack:"] + [card.attack for card in card_list])
    table.add_row(["Defence:"] + [card.defence for card in card_list])
    table.add_row(["Speed:"] + [card.speed for card in card_list])
    print(table.draw() + "\n")


def get_user_action():
    user_input = input("What would you like to do? ")

    user_input = user_input.lower().strip()

    if user_input == "help":
        help()
        return

    if user_input.startswith("play "):
        user_input = user_input[5:].strip()
        if user_input.count(" on ") == 0:
            actual_card = get_card(user_input)
            if actual_card is not None:
                play_card(actual_card)
            else:
                print("'{}' isn't a card you've got.".format(user_input))
        else:
            tokens = user_input.split(" on ")
            for index in range(1, len(tokens)):
                card1 = get_card(" on ".join(tokens[:index]))
                card2 = get_card(" on ".join(tokens[index:]))
                if card1 is not None and card2 is not None:
                    play_card_on_card(card2, card1)
                    break
            else:
                print("You have to list two valid cards to play them both.")

        return

    if user_input.startswith("attack "):
        user_input = user_input[7:].strip()
        tokens = user_input.split(" with ")
        for index in range(1, len(tokens)):
            card1 = get_card(" with ".join(tokens[:index]))
            card2 = get_card(" with ".join(tokens[index:]))
            if card1 is not None and card2 is not None:
                attack_card_with_card(card2, card1)
                return

        print("That doesn't seem to be a proper use of the 'attack' command.")
        return

    if user_input == "end":
        end_turn()
        return

    if user_input == "field":
        print("Creatures on the field:")
        print_cards(field)
        print("Unused items on the field:")
        print_cards(unused_items_on_field)
        return
    if user_input == "discard":
        print_cards(discarded_cards)
        return
    if user_input == "hand":
        print_cards(p1_hand)

    if user_input == "quit":
        print("Thanks for playing!")
        time.sleep(1)
        quit()

    print("What you entered doesn't seem to be valid. Here's some help.")
    help()


def end_turn():
    pass


def attack_card_with_card(card1, card2):
    pass


def get_card(card_name):
    """Searches your hand, the field, and the unused items on the field for the card and returns it. None otherwise"""
    actual_card = next((card for card in p1_hand if card.title.lower() == card_name), None)

    if actual_card is None:
        actual_card = next((card for card in field if card.title.lower() == card_name), None)

    if actual_card is None:
        actual_card = next((card for card in unused_items_on_field if card.title.lower() == card_name), None)

    return actual_card


def help():
    commands = {"help": "Prints this message.",
                "play <card>": "Puts the specified card on the field.",
                "play <card> on <card>": "Attempts to play the card on the other card.",
                "attack <card> with <card>": "Attempts to have your card attack the other card.",
                "end": "Ends your current turn. Play goes to the opposing player.",
                "hand": "Prints the cards in your hand.",
                "field": "Prints the cards on the field.",
                "discard": "Prints the cards in the discard.",
                "quit": "Quits the game."}
    print("Command list:")
    for command, description in commands.items():
        print("'{}' :- {}".format(command, description))


def play_card(card):
    """Puts a creature/armor/weapon into play"""
    if card not in p1_hand:
        print("You can only play cards from your hand to the field.")
        return

    if len(field) >= 4:
        print("Only 4 creatures can be on the field at one time")
        return

    if isinstance(card, Creature):
        field.append(card)
        p1_hand.remove(card)
    elif isinstance(card, Armor) or isinstance(card, Weapon):
        unused_items_on_field.append(card)
        p1_hand.remove(card)
    else:
        print("Only creatures and items can be played directly to the field. Not upgrades.")


def play_card_on_card(base_card, addon_card):
    """Attaches a card to another card"""
    if base_card not in field or base_card not in unused_items_on_field:
        print("Only cards on the field can be targeted.")
        return

    if isinstance(base_card, Creature):
        if isinstance(addon_card, Creature):
            # Evolving something I guess
            pass

        elif isinstance(addon_card, Armor):
            # Equipping new armor
            old_item = base_card.equip_armor(addon_card)
            if old_item:
                unused_items_on_field.append(old_item)

        elif isinstance(addon_card, Weapon):
            # Equipping a new weapon
            old_item = base_card.equip_weapon(addon_card)
            if old_item:
                unused_items_on_field.append(old_item)

        else:
            print("Creatures can be upgraded only through evolution.")

    if not isinstance(base_card, Upgrade) and isinstance(addon_card, Upgrade):
        # Upgrading a piece of armor or a weapon
        if isinstance(base_card, Armor) or isinstance(base_card, Weapon):
            base_card.upgrade(addon_card)
            discarded_cards.append(addon_card)


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
