from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

from kivy.config import Config
Config.set('graphics', 'width', '965')
Config.set('graphics', 'height', '305')
from utils import import_data
import random

class Card(RelativeLayout):
    card_border = ObjectProperty(None)
    card_type = ObjectProperty(None)
    card_energy = ObjectProperty(None)
    card_health = ObjectProperty(None)
    card_name = ObjectProperty(None)
    card_image = ObjectProperty(None)
    card_attack = ObjectProperty(None)
    card_damage = ObjectProperty(None)

    def __init__(self, card, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.card_type.text = repr(card.creature_type)
        self.card_energy.text = str(int(card.energy))
        self.card_health.text = "<3: {}".format(int(card.base_health))
        self.card_name.text = card.name

        self.card_attack.text = str(int(card.base_attack))
        self.card_damage.text = str(int(card.damage_negation))


class TuppyTCGGame(FloatLayout):
    def __init__(self, **kwargs):
        super(TuppyTCGGame, self).__init__(**kwargs)
        self.width = 1000
        creature_cards, armor_cards, weapon_cards, upgrade_cards = import_data()
        cards = []
        creatures = list(creature_cards.values())
        for i in range(5):
            new_card = Card(random.choice(creatures))
            new_card.pos = (15*(i+1) + 175 * i, 15)
            new_card.size_hint = (None, None)
            self.add_widget(new_card)

class TuppyTCGApp(App):
    def build(self):
        return TuppyTCGGame()


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path

        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    TuppyTCGApp().run()
