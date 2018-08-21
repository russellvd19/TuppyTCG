from PodSixNet.Connection import connection
from PodSixNet.Connection import ConnectionListener

from time import sleep


class MyNetworkListener(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))

    def Loop(self):
        self.Pump()
        connection.Pump()

    def Network(self, data):
        print('network data:', data)

    def Network_connected(self, data):
        print("connected to the server")

    def Network_error(self, data):
        print("error:", data['error'][1])

    def Network_disconnected(self, data):
        print("disconnected from the server")


class MyPlayerListener(MyNetworkListener):
    def __init__(self, *args, **kwargs):
        super(MyPlayerListener, self).__init__(*args, **kwargs)
        self.name = None
        self.game_id = None

    def register(self, name):
        print("Trying to register with the game server.")
        connection.Send({"action": "register", "name": name})

    def Network_register(self, data):
        if not data["success"]:
            print("Registration failed. {}".format(data["reason"]))
            return

        print("Successfully registered with the game server.")
        self.name = data["name"]

    def join(self, game_id=None, game_type="regular"):
        print("Trying to join a game.")
        connection.Send({"action": "join", "game_id": game_id, "game_type": game_type})

    def Network_join(self, data):
        if not data["success"]:
            print("Joining failed. {}".format(data["reason"]))
            return

        print("Successfully joined a game. Waiting to start.")
        print("Game id: {}".format(data["game_id"]))
        self.game_id = data["game_id"]

    def Network_opponent_disconnected(self, data):
        print("Opponent disconnected.")
        print(data["message"])


if __name__ == "__main__":
    myConnection = MyPlayerListener('localhost', 1337)
    myConnection.register("Skittles")
    myConnection.join()
    myConnection.Loop()
