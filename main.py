import time

from player import Player
from utils import *

creature_cards = {}
armor_cards = {}
weapon_cards = {}
upgrade_cards = {}

player_one = Player("Player 1")
player_two = Player("Player 2")


def run():
    # Create a deck for each player
    for player in [player_one, player_two]:
        new_deck = make_deck(creature_cards, armor_cards, weapon_cards, upgrade_cards)
        for card in new_deck:
            card.controller = player
        player.deck = new_deck
        player.draw_cards(amount=5)
        print("{}'s Hand".format(player.name))
        print_cards(player.hand)

    start_game(player_one, player_two)

    # Game is over now I guess
    winner = get_winner()
    if winner:
        print("Hey! {} won! Good job!".format(winner.name))
        if winner == player_one:
            loser = player_two
        else:
            loser = player_one

        end_game(winner, loser)
    else:
        print("IDK what happened, but apparently nobody won")


def start_game(p1, p2):
    # Flip a coin to see who goes first
    if random.choice([True, False]):
        first_player = p1
        second_player = p2
    else:
        first_player = p2
        second_player = p1

    print("{} is going first.".format(first_player))

    game_over = False
    while not game_over:
        print("{}'s turn.".format(first_player))
        first_player.start_turn()
        action = first_player.get_action()
        while action is not None:
            do_action(first_player, action)
            if is_game_over():
                game_over = True
                break
            action = first_player.get_action()
        first_player.end_turn()
        first_player.wait_for_turn()

        print("{}'s turn.".format(second_player))
        second_player.start_turn()
        action = second_player.get_action()
        while action is not None:
            do_action(second_player, action)
            if is_game_over():
                game_over = True
                break
            action = second_player.get_action()
        first_player.end_turn()
        first_player.wait_for_turn()


def end_game(winner, loser):
    """Gives each player all the experience they earned and resets stuff probably"""
    pass


def do_action(player, action):
    """Performs an action for a player. Will get moved to web service?"""
    pass


def is_game_over():
    """Checks if the game is over yet."""
    if player_one.shards > 10 or player_two.shards > 10:
        return True
    return False


def get_winner():
    """Returns the winning player of the current game"""
    if not is_game_over():
        print("Game isn't over yet.")
        return None

    if player_one.shards > player_two.shards:
        return player_one
    elif player_one.shards < player_two.shards:
        return player_two
    else:
        # Tiebreaker; choose a random winner for now
        return random.choice([player_one, player_two])


def attack_card_with_card(my_card, their_card):
    """Completes combat between the two cards. 'my_card' is the one attacking."""
    my_damage = my_card.attack
    if my_card.creature_type > their_card.creature_type:
        my_damage *= 1.2

    their_damage = their_card.attack
    if their_card.creature_type > my_card.creature_type:
        their_damage *= 1.2
    their_damage = their_damage // 2  # Native bonus for attackers

    damage = their_card.take_damage(my_damage)
    print("{} took {} damage.".format(their_card.name, damage))
    damage = my_card.take_damage(their_damage)
    print("{} took {} damage.".format(my_card.name, damage))

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


def play_card(player, card):
    """Puts a creature/armor/weapon into play"""
    if card not in player.hand:
        print("You can only play cards from your hand to the field.")
        return

    if len(player.field) >= 4:
        print("Only 4 creatures can be on the field at one time")
        return

    if isinstance(card, Creature):
        player.field.append(card)
        player.hand.remove(card)
    elif isinstance(card, Armor) or isinstance(card, Weapon):
        player.unused_items_on_field.append(card)
        player.hand.remove(card)
    else:
        print("Only creatures and items can be played directly to the field. Not upgrades.")


def play_card_on_card(player, base_card, addon_card):
    """Attaches a card to another card"""
    if not (player == base_card.controller == addon_card.controller):
        print("You can only play cards on your own creature.")
        return

    if base_card not in player.field and base_card not in player.unused_items_on_field:
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
                player.unused_items_on_field.append(old_item)

        elif isinstance(addon_card, Weapon):
            # Equipping a new weapon
            old_item = base_card.equip_weapon(addon_card)
            if old_item:
                player.unused_items_on_field.append(old_item)

        else:
            print("Creatures can be upgraded only through evolution.")

    if not isinstance(base_card, Upgrade) and isinstance(addon_card, Upgrade):
        # Upgrading a piece of armor or a weapon
        if isinstance(base_card, Armor) or isinstance(base_card, Weapon):
            base_card.upgrade(addon_card)
            player.discarded_cards.append(addon_card)


if __name__ == "__main__":
    creature_cards, armor_cards, weapon_cards, upgrade_cards = import_data()
    print_all_cards(creature_cards, armor_cards, weapon_cards, upgrade_cards)
    run()
