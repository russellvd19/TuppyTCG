import time

from utils import *

creature_cards = {}
armor_cards = {}
weapon_cards = {}
upgrade_cards = {}

field = []
unused_items_on_field = []
discarded_cards = []
p1_deck = []
p1_hand = []


def run():
    global p1_hand
    global p1_deck
    p1_deck = make_deck(creature_cards, armor_cards, weapon_cards, upgrade_cards)
    p1_hand = p1_deck[:5]
    print("Player 1's Hand")
    print_cards(p1_hand)

    while Creature not in [type(card) for card in p1_hand]:
        print("You're hand didn't have a creature. Redrawing...")
        random.shuffle(p1_deck)
        p1_hand = p1_deck[:5]
        print_cards(p1_hand)

    p1_deck = p1_deck[5:]

    start_turn()
    while True:
        get_user_action()


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
                addon = get_card(" on ".join(tokens[:index]))
                base = get_card(" on ".join(tokens[index:]))
                if addon is not None and base is not None:
                    play_card_on_card(base, addon)
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
        wait_for_turn()
        start_turn()
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
        return

    if user_input == "draw":
        draw_card()
        return

    if user_input == "quit":
        print("Thanks for playing!")
        time.sleep(1)
        quit()

    print("What you entered doesn't seem to be valid. Here's some help.")
    help()


def end_turn():
    print("Your turn is done. Wait for the opponent to go.")


def wait_for_turn():
    time.sleep(3)
    print("Opponent has finished their turn.")


def start_turn():
    print("It's your turn.")
    draw_card()


def draw_card():
    global p1_deck
    global p1_hand
    if len(p1_deck) <= 0:
        print("You ran out of cards. Game over for you. Bye now.")
        time.sleep(3)
        quit()

    new_card = p1_deck[0]
    print("You drew a '{}'".format(new_card.name))
    p1_hand.append(new_card)
    p1_deck = p1_deck[1:]
    print_cards(p1_hand)


def attack_card_with_card(my_card, their_card):
    """Completes combat between the two cards. 'my_card' is the one attacking."""
    my_damage = my_card.attack
    if my_card.creature_type > their_card.creature_type:
        my_damage *= 1.2

    their_damage = their_card.attack
    if their_card.creature_type > my_card.creature_type:
        their_damage *= 1.2
    their_damage = their_damage // 2  # Native bonus for attackers

    their_card.take_damage(my_damage)
    my_card.take_damage(their_damage)

    # Get all cards that may have broken, worn off, or died
    my_cards_to_discard, my_cards_to_unused = my_card.completed_attack()
    their_cards_to_discard, their_cards_to_unused = their_card.completed_attack()

    for to_discard, to_unused in [(my_cards_to_discard, my_cards_to_unused),
                                  (their_cards_to_discard, their_cards_to_unused)]:
        # Remove any cards on field to the discard
        for card in to_discard:
            card.controller.field.remove(card)
            card.controller.discarded_cards.append(card)

        # Remove any cards on field to the unused items pile
        for card in to_unused:
            card.controller.field.remove(card)
            card.controller.unused_items_on_field.append(card)

    if their_card.is_dead():
        shards, xp = their_card.value()
        my_card.controller.shards += shards
        my_card.controller.xp[my_card.name] += xp

    if my_card.is_dead():
        shards, xp = my_card.value()
        their_card.controller.shards += shards
        their_card.controller.xp[their_card.name] += xp


def attack_with(my_card):
    pass


def cancel_attack(my_card):
    pass


def get_card(card_name):
    """Searches your hand, the field, and the unused items on the field for the card and returns it. None otherwise"""
    actual_card = next((card for card in p1_hand if card.name.lower() == card_name), None)

    if actual_card is None:
        actual_card = next((card for card in field if card.name.lower() == card_name), None)

    if actual_card is None:
        actual_card = next((card for card in unused_items_on_field if card.name.lower() == card_name), None)

    return actual_card


def help():
    commands = {"help": "Prints this message.",
                "play <card>": "Puts the specified card on the field.",
                "play <card> on <card>": "Attempts to play the card on the other card.",
                "attack <card> with <card>": "Attempts to have your card attack the other card.",
                "draw": "You get to draw a card (you cheater)",
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
    if base_card not in field and base_card not in unused_items_on_field:
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


if __name__ == "__main__":
    creature_cards, armor_cards, weapon_cards, upgrade_cards = import_data()
    print_all_cards(creature_cards, armor_cards, weapon_cards, upgrade_cards)
    run()
