from functools import total_ordering


@total_ordering
class CreatureType:
    types = {
        0: "TypeA",
        1: "TypeB",
        2: "TypeC",
        3: "TypeD",
        4: "TypeE",
        5: "TypeF"
    }
    weaknesses_of = {
        0: [],
        1: [2, 3, 4],
        2: [3, 5],
        3: [4, 5],
        4: [2, 5],
        5: [1]
    }

    def __init__(self, creature_type):
        self.creature_type = creature_type

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            if other.creature_type not in CreatureType.weaknesses_of[self.creature_type]:
                if self.creature_type not in CreatureType.weaknesses_of[other.creature_type]:
                    # Not weak or strong to each other
                    return True
            return False
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ == other.__class__:
            if other.creature_type in CreatureType.weaknesses_of[self.creature_type]:
                # I am weak to them
                return True
            return False
        return NotImplemented

    def __repr__(self):
        return "{}".format(CreatureType.types.get(self.creature_type))
