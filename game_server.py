from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from time import sleep
import uuid
from game import Game


class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.name = None
        self.game = None

    def Network(self, data):
        print(data)

    def Close(self):
        if self.name is not None:
            print("{} has disconnected.".format(self.name))
            self._server.DelPlayer(self)

    # This is where I put all the commands that I receive

    def Network_register(self, data):
        print("{} trying to register.".format(data["name"]))
        self.name = data["name"]
        self._server.AddPlayer(self)

    def Network_join(self, data):
        print("{} trying to join a {} game.".format(self.name, data.get("game_type", "regular")))
        self._server.JoinGame(self, game_id=data.get("game_id"), game_type=data.get("game_type"))

    def Network_start(self, data):
        print("{} is ready to play.".format(self.name))
        self._server.ReadyPlayer(self)


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
        print("deleting {}".format(channel.addr))
        self.players.pop(str(channel.addr), None)
        if channel.game is None:
            print("No game in session")
            return

        channel.game.del_player(str(channel.addr))
        if channel.game.game_id in self.current_games:
            self.current_games.pop(channel.game.game_id, None)
            other_channel = self.players.get(channel.game.player_one.connection_address)
            if other_channel is not None:
                print("Completing active game")
                other_channel.game = None
                other_channel.Send({"action": "opponent_disconnected", "message": "You gained 5 xp?"})
                # kill the game, give xp to winner
	            # one wins, has to be told they win because disconnect
	            # pop up saying "go to menu", disable all other actions
        elif channel.game.player_one is not None:
            # There were 2 players in the game, but it hadn't started yet
            if channel.game.game_type == "regular":
                print("Continuing unstarted regular game")
                self.players[channel.game.player_one.connection_address].Send(
                    {"action": "opponent_disconnected", "message": "Finding a new challenger."})
                channel.game.accepting_players = True
                # don't kill the game
                # one has to be told the other player disconnected
                # has to be told finding new player
                # has to set the status of the player to not yet ready

            else:
                print("Leaving unstarted private game alone.")
                # It was a private game, let them know I guess
                self.players[channel.game.player_one.connection_address].Send(
                    {"action": "opponent_disconnected", "message": "Other player in private game disconnected. Waiting for idk"})

        else:
            print("Removing game with only one player")
            self.waiting_games["regular"].pop(channel.game.game_id, None)
            self.waiting_games["private"].pop(channel.game.game_id, None)

    def ReadyPlayer(self, channel):
        if channel.game is None:
            return

        game_ready = channel.game.ready_player(str(channel.addr))
        if game_ready:
            self.waiting_games["regular"].pop(channel.game.game_id, None)
            self.waiting_games["private"].pop(channel.game.game_id, None)
            self.current_games[channel.game.game_id] = channel.game
            print("Starting game {}".format(channel.game.game_id))

    def JoinGame(self, channel, game_id=None, game_type=None):
        if str(channel.addr) not in self.players:
            channel.Send({"action": "join", "success": False, "reason": "You have to register first."})
            return

        if channel.game is not None:
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
            if not game.add_player(channel.name, str(channel.addr)):
                channel.Send(
                    {"action": "join", "success": False, "reason": "Supplied game id already has two players."})
                return

        if game is None and game_type != "private":
            # Try to join a random regular game
            for possible_id, possible_game in self.waiting_games["regular"].items():
                if possible_game.add_player(channel.name, str(channel.addr)):
                    game_id = possible_id
                    game = possible_game
                    break

        if game is None:
            # No games were found, create a new one
            game = Game(game_type)
            game_id = game.game_id
            game.add_player(channel.name, str(channel.addr))
            self.waiting_games[game_type][game_id] = game

        # We've got a game id and game that the player has joined
        channel.game = game
        channel.Send({"action": "join", "success": True, "game_id": game_id})


if __name__ == "__main__":
    myserver = MyServer(localaddr=('localhost', 1337))
    myserver.Launch()
