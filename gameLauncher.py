import arcade
from src.MyGame import MyGame


def main():
    window = MyGame()
    window.setup()
    arcade.run()


main()
