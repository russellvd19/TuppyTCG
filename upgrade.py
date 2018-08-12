class Upgrade:
    def __init__(self, name, upgrades):
        self.name = name
        self.upgrades = upgrades

    def __getattr__(self, item):
        if item in self.upgrades:
            return self.upgrades[item]

    def __setattr__(self, key, value):
        self.upgrades[key] = value

    def __repr__(self):
        all_upgrades = ["\n\t{}: {}{}".format(k, "+" if v > 0 else "", v) for k, v in self.upgrades.items()]
        return "({}) {}:{}".format(self.__class__.__name__, self.name, "".join(all_upgrades))

    def __bool__(self):
        if self.name == "":
            return False
        return True
