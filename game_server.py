from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from time import sleep
import uuid
from game import Game


class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.name = None
        self.game_id = None

    def Network(self, data):
        print(data)

    def Close(self):
        self._server.DelPlayer(self)

    # This is where I put all the commands that I receive

    def Network_register(self, data):
        print("{} trying to register.".format(data["name"]))
        self.name = data["name"]
        self._server.AddPlayer(self)

    def Network_join(self, data):
        print("{} trying to join a {} game.".format(self.name, data.get("game_type", "regular")))
        self._server.JoinGame(self, game_id=data.get("game_id"), game_type=data.get("game_type"))


class MyServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = {}
        self.current_games = {}
        self.waiting_games = {"regular": {}, "private": {}}

    def Connected(self, channel, addr):
        print("New player connected.", str(addr))

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.001)

    def AddPlayer(self, channel):
        self.players[str(channel.addr)] = channel
        channel.Send({"action": "register", "success": True, "name": channel.name})

    def DelPlayer(self, channel):
        pass

    def JoinGame(self, channel, game_id=None, game_type=None):
        if str(channel.addr) not in self.players:
            channel.Send({"action": "join", "success": False, "reason": "You have to register first."})
            return

        if channel.game_id is not None:
            channel.Send({"action": "join", "success": False, "reason": "You have already joined a game."})
            return

        game = None
        if game_id is not None:
            # Get the game the id refers to, if it exists
            if game_id in self.waiting_games["regular"]:
                game = self.waiting_games["regular"][game_id]
            elif game_id in self.waiting_games["private"]:
                game = self.waiting_games["private"][game_id]
            else:
                channel.Send({"action": "join", "success": False, "reason": "Supplied game id is not an active game."})
                return

            # Make sure there is still a slot available
            if not game.add_player(channel.name):
                channel.Send(
                    {"action": "join", "success": False, "reason": "Supplied game id already has two players."})
                return

        if game is None and game_type != "private":
            # Try to join a random regular game
            for possible_id, possible_game in self.waiting_games["regular"].items():
                if possible_game.add_player(channel.name):
                    game_id = possible_id
                    game = possible_game
                    break

        if game is None:
            # No games were found, create a new one
            game_id = str(uuid.uuid4())
            game = Game()
            game.add_player(channel.name)
            self.waiting_games[game_type][game_id] = game

        # We've got a game id and game that the player has joined
        channel.Send({"action": "join", "success": True, "game_id": game_id})


if __name__ == "__main__":
    myserver = MyServer(localaddr=('localhost', 1337))
    myserver.Launch()
