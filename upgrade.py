class Upgrade:
    def __init__(self, title, attack, defence, speed):
        self.title = title
        self.attack = attack
        self.defence = defence
        self.speed = speed

    def __repr__(self):
        return "({}) {}:\n\tAttack: {}\n\tDefence: {}\n\tSpeed: {}".format(self.__class__.__name__, self.title, self.attack, self.defence, self.speed)
