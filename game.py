import time

from player import Player
from utils import *
from uuid import uuid4


class Game:
    def __init__(self, game_type):
        data_dir = os.path.join(os.path.dirname(__file__), "data/")
        self.creature_cards, self.armor_cards, self.weapon_cards, self.upgrade_cards = import_data(data_dir)
        self.player_one = None
        self.player_two = None

        self.accepting_players = True
        self.current_player = None
        self.player_resigned = None
        self.game_id = str(uuid4())
        self.game_type = game_type

    def add_player(self, name, addr):
        """Returns True if added, False if not added"""
        if self.accepting_players:
            if self.player_one is None:
                self.player_one = Player(name, addr)
                return True
            elif self.player_two is None:
                self.player_two = Player(name, addr)
                return True
        return False

    def del_player(self, addr):
        """Returns True if the game can be kept, False to be destroyed"""
        self.accepting_players = False
        if self.player_one:
            if self.player_two:
                if addr == self.player_one:
                    print("Deleting player one")
                    self.player_one = self.player_two
                    self.player_two = None
                elif addr == self.player_two:
                    print("Deleting player two")
                    self.player_two = None
                self.player_one.is_ready = False
            else:
                if addr == self.player_one:
                    self.player_one = None

    def ready_player(self, addr):
        if self.player_one is not None and self.player_one == addr:
            self.player_one.is_ready = True
        elif self.player_two is not None and self.player_two == addr:
            self.player_two.is_ready = True
        else:
            return

        if self.player_one is not None and self.player_two is not None:
            if self.player_one.is_ready and self.player_two.is_ready:
                return True
        return False


    def run(self):
        self.add_player("Tuppy")
        self.add_player("Skittles")

        # Create a deck for each player
        for player in [self.player_one, self.player_two]:
            new_deck = make_deck(self.creature_cards, self.armor_cards, self.weapon_cards, self.upgrade_cards)
            for card in new_deck:
                card.controller = player
            player.deck = new_deck
            player.draw_cards(amount=5)
            print("{}'s Hand".format(player.name))
            print_cards(player.hand)

        self.start_game()

        # Game is over now I guess
        winner = self.get_winner()
        if winner:
            print("Hey! {} won! Good job!".format(winner.name))
            if winner == self.player_one:
                loser = self.player_two
            else:
                loser = self.player_one

            self.end_game(winner, loser)
        else:
            print("IDK what happened, but apparently nobody won")

    def start_game(self):
        # Flip a coin to see who goes first
        if random.choice([True, False]):
            self.current_player = self.player_one
        else:
            self.current_player = self.player_two

        print("{} is going first.".format(self.current_player))

        game_over = False
        while not game_over:
            print("{}'s turn.".format(self.current_player))
            self.current_player.start_turn()
            action = self.current_player.get_action()
            while action.get("action", "end") is not "end":
                self.do_action(self.current_player, action)
                if self.is_game_over():
                    game_over = True
                    break
                action = self.current_player.get_action()
            self.current_player.end_turn()
            self.current_player.wait_for_turn()
            if self.current_player == self.player_one:
                self.current_player = self.player_two
            else:
                self.current_player = self.player_one

    def end_game(self, winner, loser):
        """Gives each player all the experience they earned and resets stuff probably"""
        pass

    def do_action(self, player, action):
        """Performs an action for a player. Will get moved to web service?"""

        if action["action"] == "bad_input" or action["action"] == "local_print":
            return

        if action["action"] == "play_card":
            self.play_card(player, action["card"])

        elif action["action"] == "play_card_on_card":
            self.play_card_on_card(player, action["base"], action["addon"])

        elif action["action"] == "attack_card_with_card":
            self.attack_card_with_card(player, action["attacker"], action["defender"])

        elif action["action"] == "draw":
            player.draw_cards(amount=action["amount"])

        elif action["action"] == "quit":
            self.player_resigned = player
            print("{} has quit.".format(player))
        else:
            print("'{}' doesn't exist as an action.".format(action["action"]))

    def is_game_over(self):
        """Checks if the game is over yet."""
        if self.player_resigned is not None:
            return True

        if self.player_one.shards > 10 or self.player_two.shards > 10:
            return True
        return False

    def get_winner(self):
        """Returns the winning player of the current game"""
        if not self.is_game_over():
            print("Game isn't over yet.")
            return None

        if self.player_resigned is not None:
            if self.player_resigned == self.player_one:
                return self.player_one
            return self.player_two

        if self.player_one.shards > self.player_two.shards:
            return self.player_one
        elif self.player_one.shards < self.player_two.shards:
            return self.player_two
        else:
            # Tiebreaker; choose a random winner for now
            return random.choice([self.player_one, self.player_two])

    def attack_card_with_card(self, player, my_card, their_card):
        """Completes combat between the two cards. 'my_card' is the one attacking."""

        if my_card.controller != player or their_card.controller == player:
            print("Uhh, you can only attack their creatures with your creatures.")
            return

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

    def attack_with(self, my_card):
        pass

    def cancel_attack(self, my_card):
        pass

    def help(self):
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

    def play_card(self, player, card):
        """Puts a creature/armor/weapon into play"""
        if card in player.field:
            print("That card is already in play.")
            return False

        if card not in player.hand:
            print("You can only play cards from your hand to the field.")
            return False

        if len(player.field) >= 4:
            print("Only 4 creatures can be on the field at one time")
            return False

        if isinstance(card, Creature):
            player.field.append(card)
            player.hand.remove(card)
            return True
        elif isinstance(card, (Armor, Weapon)):
            player.unused_items_on_field.append(card)
            player.hand.remove(card)
            return True
        else:
            print("Only creatures and items can be played directly to the field. Not upgrades.")
            return False

    def play_card_on_card(self, player, base_card, addon_card):
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
    game = Game()
    game.run()
