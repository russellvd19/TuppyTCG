from kivy.app import App
from kivy.uix.widget import Widget


class TuppyTCGGame(Widget):
    pass


class TuppyTCGApp(App):
    def build(self):
        return TuppyTCGGame()


if __name__ == '__main__':
    TuppyTCGApp().run()
