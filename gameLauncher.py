import arcade
from src.gameClass import MyGame


def main():
    window = MyGame()
    window.setup()
    arcade.run()


main()
