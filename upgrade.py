from card import Card


class Upgrade(Card):
    def __init__(self, name, upgrades):
        super().__init__()
        self.name = name
        self.upgrades = upgrades

    def __getattr__(self, item):
        # For when upgrades doesn't exist yet. Otherwise infinite recursion b/c next if statement
        if item == "upgrades":
            raise AttributeError

        if item in self.upgrades:
            return self.upgrades[item]
        else:
            raise AttributeError

    def __repr__(self):
        all_upgrades = ["\n  {}: {}{}".format(k, "+" if v > 0 else "", v) for k, v in self.upgrades.items()]
        return "({})\n{}:{}".format(self.__class__.__name__, self.name, "".join(all_upgrades))

    def __bool__(self):
        if self.name == "":
            return False
        return True
