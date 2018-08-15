class Card:
    _next_id = 0

    def __init__(self):
        self.unique_id = Card.next_id()
        self.controller = None

    @staticmethod
    def next_id():
        id = Card._next_id
        Card._next_id += 1
        return id

    def __hash__(self):
        return hash(self.unique_id)