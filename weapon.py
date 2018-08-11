from item import Item

class Weapon(Item):
    def __init__(self, title, attack, defence, speed):
        super().__init__(title, attack, defence, speed)
