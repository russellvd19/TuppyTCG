from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.graphics import Color

from kivy.config import Config

Config.set('graphics', 'width', '965')
Config.set('graphics', 'height', '635')
from utils import import_data
import random


class CardSlot(Widget):
    card_widget = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CardSlot, self).__init__(**kwargs)
        self.card = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("CardSlot was selected")
            if Card.card_selected is not None:
                if self.card is None:
                    self.card = Card.card_selected
                    self.card_widget = Card.card_widget
                    Card.card_widget.pos = self.pos


class Field(BoxLayout):
    card1 = ObjectProperty(None)
    card2 = ObjectProperty(None)
    card3 = ObjectProperty(None)
    card4 = ObjectProperty(None)


class Card(RelativeLayout):
    border_color = ListProperty([.1, .1, 1, .9])
    background_color = ListProperty([1, 1, 1, .5])

    card_selected = None
    card_widget = None

    def __init__(self, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.card = None
        self.unselected_color = [.1, .1, 1, .9]
        self.selected_color = [1, .1, .1, .9]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if Card.card_widget == self:
                self.unselect()
            elif Card.card_widget is not None:
                Card.card_widget.unselect()
                self.select()
            else:
                self.select()
            return True
        return False

    def unselect(self):
        self.border_color = self.unselected_color
        Card.card_selected = None
        Card.card_widget = None

    def select(self):
        self.border_color = self.selected_color
        Card.card_selected = self.card
        Card.card_widget = self


class CreatureCard(Card):
    card_type = ObjectProperty(None)
    card_energy = ObjectProperty(None)
    card_health = ObjectProperty(None)
    card_name = ObjectProperty(None)
    card_image = ObjectProperty(None)
    card_attack = ObjectProperty(None)
    card_damage = ObjectProperty(None)

    def __init__(self, card, **kwargs):
        super(CreatureCard, self).__init__(**kwargs)
        self.card = card
        self.card_type.text = repr(card.creature_type)
        self.card_energy.text = str(int(card.energy))
        self.card_health.text = "<3: {}".format(int(card.base_health))
        self.card_name.text = card.name

        self.card_attack.text = str(int(card.base_attack))
        self.card_damage.text = str(int(card.damage_negation))


class TuppyTCGGame(FloatLayout):
    def __init__(self, **kwargs):
        super(TuppyTCGGame, self).__init__(**kwargs)
        creature_cards, armor_cards, weapon_cards, upgrade_cards = import_data()
        cards = []
        creatures = list(creature_cards.values())
        for i in range(5):
            new_card = CreatureCard(random.choice(creatures))
            new_card.pos = (15 * (i + 1) + 175 * i, 15)
            new_card.size_hint = (None, None)
            self.add_widget(new_card)

        field = Field()
        field.pos = (92.5, 305)
        field.size_hint = (None, None)
        self.add_widget(field)

    def on_touch_down(self, touch):
        card_touched = super(TuppyTCGGame, self).on_touch_down(touch)
        if not card_touched and Card.card_selected is not None:
            Card.card_widget.unselect()


class TuppyTCGApp(App):
    def build(self):
        return TuppyTCGGame()


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path

        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    TuppyTCGApp().run()
