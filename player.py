import random
import time
from utils import print_cards


class Player():

    def __init__(self, name):
        self.name = name
        self.field = []
        self.unused_items_on_field = []
        self.discarded_cards = []
        self.deck = []
        self.hand = []
        self.xp = {}
        self.shards = 0

    def start_turn(self):
        print("It's your turn.")
        self.draw_cards(amount=1)

    def end_turn(self):
        print("Your turn is done. Wait for the opponent to go.")

    def wait_for_turn(self):
        print("Waiting for opponent to finish.")

    def shuffle_into_deck(self, card_list):
        self.deck.extend(card_list)
        random.shuffle(self.deck)

    def draw_cards(self, amount=1):
        if len(self.deck) < amount:
            print("You ran out of cards. Game over for you. Bye now.")
            time.sleep(3)
            quit()

        self.hand.extend(self.deck[:amount])
        self.deck = self.deck[amount:]

    def get_action(self):
        user_input = input("What would you like to do? ")
        user_input = user_input.lower().strip()

        if user_input == "help":
            help()
            return {"action": "local_print"}

        if user_input.startswith("play "):
            user_input = user_input[5:].strip()
            if user_input.count(" on ") == 0:
                actual_card = self.get_card(user_input)
                if actual_card is not None:
                    return {"action": "play_card", "card": actual_card}
                else:
                    print("'{}' isn't a card you've got.".format(user_input))
                    return {"action": "bad_input"}
            else:
                tokens = user_input.split(" on ")
                for index in range(1, len(tokens)):
                    addon = self.get_card(" on ".join(tokens[:index]))
                    base = self.get_card(" on ".join(tokens[index:]))
                    if addon is not None and base is not None:
                        return {"action": "play_card_on_card", "base": base, "addon": addon}

                else:
                    print("You have to list two valid cards to play them both.")
                    return {"action": "bad_input"}

        if user_input.startswith("attack "):
            user_input = user_input[7:].strip()
            tokens = user_input.split(" with ")
            for index in range(1, len(tokens)):
                card1 = self.get_card(" with ".join(tokens[:index]))
                card2 = self.get_card(" with ".join(tokens[index:]))
                if card1 is not None and card2 is not None:
                    return {"action": "attack_card_with_card", "attacker": card2, "defender": card1}

            print("That doesn't seem to be a proper use of the 'attack' command.")
            return {"action": "bad_input"}

        if user_input == "end":
            return {"action": "end"}

        if user_input == "field":
            print("Creatures on the field:")
            print_cards(self.field)
            print("Unused items on the field:")
            print_cards(self.unused_items_on_field)
            return {"action": "local_print"}

        if user_input == "discard":
            print_cards(self.discarded_cards)
            return {"action": "local_print"}

        if user_input == "hand":
            print_cards(self.hand)
            return {"action": "local_print"}

        if user_input == "draw":
            return {"action": "draw", "amount": 1}

        if user_input == "quit":
            print("Thanks for playing!")
            return {"action": "quit"}

        print("What you entered doesn't seem to be valid. Here's some help.")
        help()
        return {"action": "local_print"}

    def get_card(self, card_name):
        """Searches your hand, the field, and the unused items on the field for the card and returns it. None otherwise"""
        actual_card = next((card for card in self.hand if card.name.lower() == card_name), None)

        if actual_card is None:
            actual_card = next((card for card in self.field if card.name.lower() == card_name), None)

        if actual_card is None:
            actual_card = next((card for card in self.unused_items_on_field if card.name.lower() == card_name), None)

        return actual_card

    def __repr__(self):
        return self.name
